import os
import csv
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pprint import pformat
import sys

load_dotenv()  

BASE_URL = "https://api.veryfi.com/api/v8/"
CLIENT_ID = os.getenv("client_id")
USERNAME = os.getenv("username")
API_KEY = os.getenv("api_key")

AUTH_HEADER = f"apikey {USERNAME}:{API_KEY}"
HEADERS = {
    "CLIENT-ID": CLIENT_ID,
    "AUTHORIZATION": AUTH_HEADER,
}


output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
csv_filename = output_dir / f"receipt_export_{timestamp}.csv"

CSV_HEADERS = [
    "veryfi_document_id",
    "order_date",
    "vendor",
    "order_total",
    "item",
    "quantity",
    "price",
]


def coalesce(*args):
    """Return the first non-empty value."""
    for arg in args:
        if arg:
            return arg
    return ""

with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADERS)


    resp = requests.get(f"{BASE_URL}partner/documents?status=processed", headers=HEADERS)
    resp.raise_for_status()
    documents = resp.json().get("documents", [])
    
    if len(documents) < 1:
        print("No unextracted documents.")
        sys.exit()

    for doc in documents:
        doc_id = doc.get("id")
        vendor = coalesce(
            doc.get("vendor", {}).get("name"),
            doc.get("vendor", {}).get("raw_name"),
        )
        order_date = doc.get("date")
        order_total = doc.get("total")

        # collect rows for this document
        rows = []
        for line in doc.get("line_items", []):
            description = coalesce(
                line.get("description"),
                line.get("full_description"),
                line.get("text"),
            )
            price = line.get("total")
            quantity = line.get("quantity")

            rows.append([
                doc_id,
                order_date,
                vendor,
                order_total,
                description,
                quantity,
                price,
            ])

        # write all rows for this document
        writer.writerows(rows)

        # update document status to reviewed
        note_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        update_body = {
            "status": "reviewed",
            "notes": f"Extracted by script on {note_time}",
        }
        put_url = f"{BASE_URL}partner/documents/{doc_id}"
        update_resp = requests.put(put_url, headers=HEADERS, json=update_body)
        update_resp.raise_for_status()

print(f"Export complete. CSV saved to {csv_filename}")
