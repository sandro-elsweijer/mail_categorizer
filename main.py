import ocrmypdf
import configparser
from datetime import datetime
import PyPDF2
import re
import os

def find_pdf_files(path):
  """Returns the paths to all pdf files in the ./unsorted/ folder
  
  Args:
      path (string): path/to/pdf/files

  Returns:
      list: List of all pdf file paths
  """

  paths_to_files = []
  for root, dirs, files in os.walk(os.path.abspath(path), topdown=False):
    for file in files:
      # Check if file is pdf, case insensitive.
      if file[-4:].lower() == ".pdf":
        paths_to_files.append(os.path.join(root, file))
  return paths_to_files

def ocr_files(files):
  """Adds OCR information to all listed pdf files

  Args:
      files (list): List of pdf file paths
  """

  for file in files:
    ocrmypdf.ocr(file, file, deskew=True)

def categorize_files(files, categories):
  """Categorizes given pdf files into given categories. 
     Successfully categorized files are saved in the given category instance in 
     the category list. Files with no or multiple matching categories get their own category.

  Args:
      files (list): List of all pdf file paths
      categories (list): List of all defined categories. 
                         Categorized files are saved in the categories in this list.
  """
  
  
  # All files with no match or multiple matches get saved in the 
  # no_match and multiple_matches list.
  no_match = []
  multiple_matches = []
  for file in files:
    # in_category saves which category a file belogs to
    in_category = ""
    pdf = PyPDF2.PdfFileReader(file)
    pdf_text = ""
    for i in range(pdf.getNumPages()):
      page = pdf.getPage(i)
      pdf_text += page.extractText()
    for category in categories:
      # Check if all keywords are in pdf
      all_keywords_in_pdf = True
      for keyword in category.keywords:
        if not re.search(keyword, pdf_text, re.IGNORECASE):
          all_keywords_in_pdf = False
      if all_keywords_in_pdf:
        if len(in_category) > 0:
          # File is already categorized, therefore it gets saved in 
          # the multiple_matches list
          multiple_matches.append(file)
          break
        else:
          in_category = category.foldername
    if len(in_category) == 0:
      # No match was found, file gets saved in the no_match list
      no_match.append(file)
    else:
      # Only one matching category was found, save file in category
      for category in categories:
        if in_category == category.foldername:
          category.files.append(file)
          break
  # Add not categorizable files as categories
  if len(no_match):
    categories.append(Category("no_match", [], no_match))
  if len(multiple_matches):
    categories.append(Category("multiple_matches", [], multiple_matches))

def read_config(filepath):
  """Reads the config and saves the defined categories as a list

  Args:
      filepath (string): Path to the configfile

  Returns:
      list: List of all defined categories
  """
  categories = []
  config = configparser.ConfigParser()
  config.read("/home/sandro/workspace/pdfsort/config.ini")
  config = config["CATEGORIES"]
  for key in config:
    keywords = config[key].split(" ")
    categories.append(Category(key, keywords))
  return categories

def move_files_into_categories(categories):
  """Moves files into their category folders. 
     Alters filenames to timestamps.

  Args:
      categories (list): List of all categories and their files
  """
  for category in categories:
    if not os.path.isdir(category.foldername):
      os.makedirs(category.foldername)
    for file in category.files:
      path = os.path.split(file)[0]
      new_file = os.path.join(path, "..", 
                              category.foldername, 
                              datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.pdf"))
      os.rename(file, new_file)


class Category():
    def __init__(self, foldername, keywords = [], files = []):
      """Class, which can save the foldername, keywords and the 
         files belonging to a category

      Args:
          foldername (string): Name of the folder to save the pdfs in
          keywords (list): List of all keywords which should appear in a pdf 
                           belonging to this category
          files (list): List of all files in this category
      """
      
      self.foldername = foldername
      self.keywords = keywords
      self.files = files

if __name__ == '__main__':
  files = find_pdf_files("unsorted/")
  #ocr_files(files)
  categories = read_config("config.ini")
  categorize_files(files, categories)
  move_files_into_categories(categories)
