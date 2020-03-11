import PyPDF2 as py_pdf
import re
import os
from docx import Document
import pandas as pd
import extract_email as em
import pdfextract as pe
import phonenumber as pn
import random
import skills as sk

file_list = os.listdir('C:/Users/TarunVashishth/Desktop/UI/Resume')
l = []
different_file = []
bad_file = []
i = 0

import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern])
        
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
    print(span.text)

for file_name in file_list:
    try:
        i = i + 1
        file_ext = file_name.split('.')[-1]

        mail = ""

        if (file_ext == 'docx'):
            print(str(i)+' '+ file_name)
            f = open('C:/Users/TarunVashishth/Desktop/UI/Resume/' + file_name, 'rb')
            file = Document(f)
            text = ""
            for para in file.paragraphs:
                text += para.text
                mail = em.extract_email_addresses(text)
                print("Email:", mail)
                f.close()

        elif (file_ext == 'pdf'):
            print(str(i)+' '+ file_name)
            full_file_name = 'C:/Users/TarunVashishth/Desktop/UI/Resume/' + file_name
            pagecontent = pe.pdfextract(full_file_name)
            # extract_name(pagecontent)
            mail = em.extract_email_addresses(pagecontent)

            phonenumbers = pn.extract_phone_numbers(pagecontent)
            if phonenumbers == []:
                phonenumber = 'NA'
            else:
                phonenumber = random.choice(phonenumbers)
            sk.extract_skills(pagecontent)
            

        elif (file_ext == 'doc'):
            print('C:/Users/TarunVashishth/Desktop/UI/Resume/' + file_name)
            pdfFileObj = open(file_name, 'rb')
            pdfReader = py_pdf.PdfFileReader(pdfFileObj)
            page = pdfReader.getPage(0)
            pagecontent = page.extractText()
            mail = em.extract_email_addresses(pagecontent)
            pdfFileObj.close()

        else:
            different_file.append(file_name)
            
        dict = {}
        dict['S.No.'] = i
        # dict['Name'] = person_name
        dict['Phone Number'] = phonenumber
        # dict['Skills']= skill_set 

        if (len(mail) > 0):
            dict['mail id'] = mail
            l.append(dict)
        else:
            dict['mail id'] = 'NA'
            l.append(dict)

        # dict['Skills'] = skill_set

    except Exception as e:
        bad_file.append(file_name)

print(l)

# df = pd.DataFrame(l)
# df.to_csv('C:/Users/TarunVashishth/Desktop/UI/data5.csv')

# with open('different_file.txt', 'w') as f:
#     for item in different_file:
#         f.write("%s\n" % item)

# with open('bad_file.txt', 'w') as f:
#     for item in bad_file:
#         f.write("%s\n" % item)

