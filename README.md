# Mail categorizer
I am too lazy to sort my scanned mail by hand, so I automated it.
It can be used as a cron job to add ocr information to scanned pdfs in a specific folder
and to sort the pdfs according to predefined keywords.

## Disclaimer
This is just a private project. Please back up your data regularly. I cannot guarantee that some bugs or misusage corrupt or delete your data.

## Installation

The package needs `tesseract-ocr` to be installed:
```
sudo apt-get install tesseract-ocr
```

To install the mailcategorizer we execute:
```
git clone git@github.com:sandro-elsweijer/mailcategorizer.git
cd mail_categorizer
pip install .
```

## Usage
We can define the directory, where the scan pdfs are located in the `config.yml`.
We also define, into which folder the files should be sorted.

Lastly, we define the categories for our pdfs. The key value is the name of the folder the pdfs of this category get sorted into. The value is a semicolon-separated list of all keywords, which have to appear in the pdf.

pdfs which match in multiple categories are saved into a dedicated `multiple_matches` folder. pdfs with no match are saved into the `no_matches` folder.

When calling the mailcategorizer, we have to provide it with the location of the config file:
```
mailcategorizer path/to/config.yml
```

I suggest to automate this process with a cron job, so every time a document is scanned, it gets sorted automatically.
