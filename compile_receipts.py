base_url = 'https://api.veryfi.com/api/v8/'
client_id = process.env('client_id')
auth_header = 'apikey ${process.env('username')}:${process.env('api_key')}'
headers = {
    'CLIENT-ID': client_id,
    'AUTHORIZATION': auth_header
}

# use os.path.join instead of string interpolation
csv_filename = output/receipt_export_yyyy_mm_dd_ss_xxx.csv

csv_headers = [veryfi_document_id, order_date, vendor, order_total, item, quantity, price]

#write header row to csv

#request all documents from https://api.veryfi.com/api/v8/partner/documents?status=processed

#loop through all documents:
    #id = response['id']
    #vendor = coalesce(response['vendor']['name'],response['vendor']['raw_name'])
    #order_date = response['date']
    #order_total = response['total']
    #loop through response['line_items']:
        #description = coalesce(description, full_description, text) 
        # price = total
        # quantity = quantity
        # save row but don't write yet: [id, order_date, vendor, order_total, description, price, quantity]
        
    # when all line items are complete:
        # write saved row to csv
        # update document using PUT https://api.veryfi.com/api/v8/partner/documents/{id}
        # headers same as above
        # body = {
        #    "status":"reviewed"
        #    "notes" : "extracted by script on YYYY-MM-DD HH:MM:SS.XXX" 
        #}

# when all documents complete:
# close csv file
