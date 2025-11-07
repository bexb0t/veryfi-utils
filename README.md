A silly little script for downloading receipts that have been forwarded to VeryFi for OCR parsing: https://docs.veryfi.com/

Currently just dumps everything it reads to a csv for import elsewhere. Maybe it'll become less silly and less little at tax time. 

To use it, you must first have created a free tier "Platform API Account" with Veryfi. When you do this an email address @veryfi.cc should automatically be created and you can forward receipts to that to put them in your "inbox".  To get that email address go to the "Collect" button in the upper right of the dashboard found at https://app.veryfi.com. You'll get a dialog to drag and drop files, which you can do as well. But also on the right it will say "or email them to <email address here>"

Once you have some files in the inbox, you'll want to take a look at them and make sure it looks like they're parsing correctly and saving the line item data you expect. Shopify receipts have worked fine for me so far. 

Once you have all that going, clone this repo and create a text file with the following contents:
```bash
client_id='your_client_id'
username='your_username'
api_key='your_api_key'
```

Name it .env and save it to the same directory as compile_receipts.py. 


Then run it using poetry:
```bash
poetry run python compile_receipts.py
```

The project requires poetry and python version 3.14. I committed a pyenv file but whatever python version management you want to use is your business. You can probably also get away with an older version of python by changing the min version in pyproject.toml.

I made this public for no good reason really. Nothing in here is terribly innovative. Feel free to fork, clone, or copy paste if it pleases you but I don't plan to provide any support lol. No official license terms, just be excellent to each other. 
