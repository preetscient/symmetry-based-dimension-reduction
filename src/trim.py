import os
import re
import ast

testfiles = ['divorce.gap',
'mammalia-voles-bhp-trapping-63.gap',
'mammalia-voles-rob-trapping-05.gap',
'mammalia-asianelephant.gap',
'mammalia-voles-rob-trapping-14.gap',
'mammalia-voles-plj-trapping-52.gap',
'mammalia-voles-rob-trapping-29.gap',
'mammalia-voles-rob-trapping-15.gap']

current_file_path = os.path.abspath(__file__)
base_path = os.path.join(current_file_path, '..','..')
base_path = os.path.normpath(base_path)

gap_folder = os.path.join(base_path,'data','external','3_gap_readable_automorphism_data','networkrepository')
def extract_substrings_from_files(folder_path):
    extracted_data = {}

    # Iterate over each file in the folder
    # for filename in os.listdir(folder_path):
    for filename in testfiles:
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()

                # Find all substrings between 'z:=' and ';;'
                matches = re.findall(r'z:=\[\s*\'(.*?)\'\s*\];;', file_contents, re.DOTALL)
                
                # Add to dictionary with filename as key
            
                
                print(matches)

    return extracted_data


extracted_list = extract_substrings_from_files(gap_folder)  




