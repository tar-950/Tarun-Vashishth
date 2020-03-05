from collections import Counter
from IPython.display import clear_output
from textblob import TextBlob
import io, re, nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
from nltk.corpus import wordnet
import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import perf_counter, sleep
from pprint import pprint
import json, zipfile, PyPDF2, docx, spacy
from spacy.matcher import Matcher
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage


# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

#txt = read_pdf(r'C:\Users\KailashChandraOli\Desktop\Project\Anushree hms.pdf')
# txt = read_pdf(r'C:\Users\TarunVashishth\Desktop\aditya bhartia.pdf')
    
class Parse():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []
    #path = r'C:\Users\TarunVashishth\Desktop\Language_Processing-master'

    def __init__(self, verose):
        print('Starting Programme')
        #fields = ["name", "address", "email", "phone", "mobile", "telephone","residence status","experience","degree","cainstitute","cayear","caline","b.cominstitute","b.comyear","b.comline","icwainstitue","icwayear","icwaline","m.cominstitute","m.comyear","m.comline","mbainstitute","mbayear","mbaline"]
        
        #Glob module matches certain patterns
        doc_files = glob.glob("Resume/*.doc")
        docx_files = glob.glob("Resume/*.docx")
        pdf_files = glob.glob("Resume/*.pdf")
        rtf_files = glob.glob("Resume/*.rtf")
        text_files = glob.glob("Resume/*.txt")

        files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)

        files = list(files)
        print(files)
        print ("{} files identified" .format(len(files)))
 
        for f in files:
            print("Reading File {}" .format(f))

            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            extension = f.split(".")[-1]

            info['extension'] = extension 
            inputString =  self.readFile(f, extension)

            # myString = ' '.join(inputString).split();
            # myString = myString.replace('\\n','').split(' ')
            # info['fileName'] = f

            name = self.extract_name(inputString)
            phonenumber = self.extract_phone_numbers(inputString)
            email = self.extract_email_addresses(inputString)
            # experience = self.extract_experience(inputString)
            info = {'Name': name, 'Phone Number':str(phonenumber), 'E-mail':str(email)}
            self.information.append(info)
        print(self.information)


    def readFile(self, fileName, extension):

        if extension == "txt":
            f = open(fileName, 'r')
            string = b'f.read()'
            print(string)
            f.close() 
            return string

        elif extension == "doc":
            # Run a shell command and store the output as a string
            # Antiword is used for extracting data out of Word docs. Does not work with docx, pdf etc.
            return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

        # elif extension == "docx":
        #     try:
        #         print('hello')
        #         return convertDocxToText(fileName)
        #     except:
        #         return ''
        #         pass


        elif extension == "pdf":
            try:
                text = self.read_pdf(fileName)
                return text
            except:
                return ''
                pass

        else:
            print ('Unsupported format')
            return ''
    
    def read_pdf(self, path):
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

    # def convertDocxToText(self, filename):
    #     doc = b'docx.Document(filename)'
    #     fullText = []
    #     for para in doc.paragraphs:
    #         fullText.append(para.text)
    #     text = '\n'.join(fullText)
    #     print(text)
    #     return text
    
    def extract_name(self, resume_text):
        nlp_text = nlp(resume_text)

        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        matcher.add('NAME', [pattern])
        
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    def extract_phone_numbers(self, string):
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(string)
        return [re.sub(r'\D', '', number) for number in phone_numbers]

    def extract_email_addresses(self, string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        return r.findall(string)

    # def extract_experience(self, string):
    #     r = re.compile(r'\d[0-9]{1}')
    #     return r.findall(string)



if __name__ == "__main__":
    verose = False
    if "-v" in str(sys.argv):
        verose = True
    p = Parse(verose)

