#!/usr/bin/env python3

from PyPDF2 import PdfReader, PdfWriter
import re
import glob
import logging

begin_keyword = 'Resume Profile'
end_keyword = 'If you have any questions,'

total_num_of_begin = 0
total_num_of_end = 0

files_created = 0

def save_resume(file, first_name: str, last_name: str, start_page_num: int, end_page_num: int):
  global files_created
  pdf_writer = PdfWriter()

  for i in range(start_page_num, end_page_num + 1):
    pdf_writer.add_page(file.pages[i])

  files_created += 1
  out_file_name = './output/' + str(files_created) + '_' + first_name + '_' + last_name + '.pdf'

  pdf_writer.write(out_file_name)

def split_resumes(pdf_file):
  global total_num_of_begin
  global total_num_of_end

  found_resume = False

  first_name = None
  last_name = None

  start_page_num = -1
  end_page_num = -1

  for page_obj in pdf_file.pages:
    page_content = page_obj.extract_text()
    if re.search(begin_keyword, page_content):
      total_num_of_begin += 1
      start_page_num = PdfReader.get_page_number(self=pdf_file, page=page_obj)
      found_resume = False
    if re.search(end_keyword, page_content):
      total_num_of_end += 1
      end_page_num = PdfReader.get_page_number(self=pdf_file, page=page_obj)
      found_resume = True

    # Get first name
    search_first_name = re.search('(?<=First Name)(.*)', page_content)
    if search_first_name:
      first_name = search_first_name.group(1).replace(' ', '')

    # Get last name
    search_last_name = re.search('(?<=Last Name)(.*)', page_content)
    if search_last_name:
      last_name = search_last_name.group(1).replace(' ', '')

    if found_resume and first_name and last_name:
      save_resume(pdf_file, first_name, last_name, start_page_num, end_page_num)
      first_name = None
      last_name = None
      found_resume = False


def main():
  list_of_input_files = glob.glob1('./input',"*.pdf")
  num_of_file = len(list_of_input_files)

  print('Number of files detected in the input folder: ', num_of_file)

  for file_name in list_of_input_files:
    pdf_file = PdfReader('./input/' + file_name)
    split_resumes(pdf_file)

  if total_num_of_begin != total_num_of_end:
    logging.error(
      'The number of start line detected does not match the end line detected! Corrupted files were generated.\n'
      + 'total_num_of_begin: ' + str(total_num_of_begin)
      + 'total_num_of_end: ' + str(total_num_of_end)
      )

  print('Generated ', str(files_created), ' files of PDF, can be found in the output folder.')

main()
