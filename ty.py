from collections import Counter
from IPython.display import clear_output
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from textblob import TextBlob
import pandas as pd
import io
import os
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
stop = stopwords.words('english')
from nltk.corpus import wordnet
import csv
import re
import spacy
import sys
import importlib
import sys, getopt
from bs4 import BeautifulSoup
import urllib3
importlib.reload(sys)

def read_pdf(path):
    print(path)
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True): 
        interpreter.process_page(page)
    text = retstr.getvalue()
    text = " ".join(text.replace(u"\xa0", " ").strip().split())  
    fp.close()
    device.close()
    retstr.close()
    return text

#txt = read_pdf(r'C:\Users\KailashChandraOli\Desktop\Project\Anushree hms.pdf')
resume_string = read_pdf(r'C:\Users\TarunVashishth\Desktop\himanshu_kholiya_resumeNEW.pdf')

# self.getExperience(self.inputString, info, debug=False)

# def extract_skills(nlp_text, noun_chunks):
#         '''
#         Helper function to extract skills from spacy nlp text

#         :param nlp_text: object of `spacy.tokens.doc.Doc`
#         :param noun_chunks: noun chunks extracted from nlp text
#         :return: list of skills extracted
#         '''
#         tokens = [token.text for token in nlp_text if not token.is_stop]
#         data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
#         skills = list(data.columns.values)
#         skillset = []
#         # check for one-grams
#         for token in tokens:
#             if token.lower() in skills:
#                 skillset.append(token)
        
#         # check for bi-grams and tri-grams
#         for token in noun_chunks:
#             token = token.text.lower().strip()
#             if token in skills:
#                 skillset.append(token)
#         return [i.capitalize() for i in set([i.lower() for i in skillset])]


# sys.setdefaultencoding('utf8')

# sys.setdefaultencoding('utf8')

# from urllib3 import urlopen

#Converting pdf to string
resume_string1 = resume_string
#Removing commas in the resume for an effecient check
resume_string = resume_string.replace(',',' ')
#Converting all the charachters in lower case
resume_string = resume_string.lower()

# with open(r'C:\Users\TarunVashishth\Desktop\resume-parser-master (1)\resume-parser-master\techatt.csv', 'rt') as f:
#     reader = csv.reader(f)
#     your_listatt = list(reader)
with open(r"C:\Users\TarunVashishth\Desktop\resume-parser-master (1)\resume-parser-master\skill.csv", 'rt') as f:
    reader = csv.reader(f)
    your_list = list(reader)
    your_list = your_list[0]
    your_list = [word.lower() for word in your_list]


with open(r"C:\Users\TarunVashishth\Desktop\resume-parser-master (1)\resume-parser-master\nontechnicalskills.csv", 'rt') as f:
    reader = csv.reader(f)
    your_list1 = list(reader)
#Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
s = set(your_list)

# s1 = your_list
# s2 = your_listatt
# skillindex = []
skills = []
# skillsatt = []
print('\n')

for word in resume_string.split(" "):
    if word in s:
        skills.append(word)
skills1 = list(set(skills))
print(skills1)
print('\n')
# print("Following are his/her Technical Skills")
# print('\n')
# np_a1 = np.array(your_list)
# for i in range(len(skills1)):
#     item_index = np.where(np_a1==skills1[i])
#     skillindex.append(item_index[1][0])

# nlen = len(skillindex)
# for i in range(nlen):
#     print(skills1[i])
#     print(s2[0][skillindex[i]])
#     print('\n')

# #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
# s1 = set(your_list1[0])
# nontechskills = []
# for word in resume_string.split(" "):
#     if word in s1:
#         nontechskills.append(word)
# nontechskills = set(nontechskills)
# print('\n')

# print("Following are his/her Non Technical Skills")
# list5 = list(nontechskills)
# print('\n')
# for i in range(len(list5)):
#     print(list5[i])
# print('\n \n')


# def getExperience(self,inputString,infoDict,debug=False):
#         experience=[]
#         try:
#             for sentence in self.lines:#find the index of the sentence where the degree is find and then analyse that sentence
#                     sen=" ".join([words[0].lower() for words in sentence]) #string of words in sentence
#                     if re.search('experience',sen):
#                         sen_tokenised= nltk.word_tokenize(sen)
#                         tagged = nltk.pos_tag(sen_tokenised)
#                         entities = nltk.chunk.ne_chunk(tagged)
#                         for subtree in entities.subtrees():
#                             for leaf in subtree.leaves():
#                                 if leaf[1]=='CD':
#                                     experience=leaf[0]
#         except Exception as e:
#             print (traceback.format_exc())
#             print (e) 
#         if experience:
#             infoDict['experience'] = experience
#         else:
#             infoDict['experience']=0
#         if debug:
#             print ("\n", pprint(infoDict), "\n")
#             code.interact(local=locals())
#         return experience



