# Mail categorizer
I am too lazy to sort my mail by hand, so I scripted this tool to do it for me.
It can be used as a daemon to add ocr information to scanned pdfs in a specific folder
and to sort the pdfs according to predefined keywords.

## Disclaimer
This is just a private project. Please back up your data regularly. I cannot guarantee that some bugs or misusage corrupt or delete your data.

## Usage
Define categories in the `config.ini`. The category is used as the folder name for the categorized pdfs. The script will search for each space-separated keyword inside each pdf and categorize the pdfs according to the occurring keywords in the pdf. The script will save each uncategorizable in a
`no_match` or a `multiple_matches` folder. If a pdf appears in there you have to tweak your keywords.

Run the python script and specify the folder with the uncategorized mail scans (e.g. where your scanner saves them automatically) and the location of your `config.ini`.
