from collections import Counter
from textblob import TextBlob
import io, re, nltk
from datetime import date 
from nltk.corpus import stopwords
stop = stopwords.words('english')
import nltk, os, subprocess, glob, sys, random
import PyPDF2, docx, spacy
from spacy.matcher import Matcher
from datetime import date
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

        print ("{} files identified" .format(len(files)))
 
        for f in files:
            print("Reading File")

            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            extension = f.split(".")[-1]

            info['extension'] = extension 
            inputString =  self.readFile(f, extension)

            # myString = ' '.join(inputString).split();
            # myString = myString.replace('\\n','').split(' ')
            # info['fileName'] = f

            name = self.extract_name(inputString)
            email = self.extract_email_addresses(inputString)
            phonenumbers = self.extract_phone_numbers(inputString)
            print(phonenumbers)
            if phonenumbers == []:
                phonenumber = 'NA'
            else:
                phonenumber = random.choice(phonenumbers)

            # skill = self.extract_skills(inputString)
            # experience = self.get_work(inputString)
            info = {'Name': name, 'Phone Number':str(phonenumber), 'E-mail':str(email)}
            self.information.append(info)


    def readFile(self, fileName, extension):

        if extension == "txt":
            f = open(fileName, 'r')
            string = b'f.read()'
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
        phonelist = None
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(string)
        phonelist = [re.sub(r'\D', '', number) for number in phone_numbers if number is not None]
        return phonelist

    def extract_email_addresses(self, string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        e_mail=r.findall(string)[0]
        return e_mail

    # def get_work(self,string):
    #     experience = []
    #     for each in self.work:
    #         index = self.headings[self.headings.index(each[0])+1]
    #         experience.append("\n".join(self.content[each[0]+1:index]))
    #     if len(experience) == 1:
    #         return experience[0]
    #     else:
    #         return experience

    # def parse(self):
    #     name = dict()
    #     work_experience = dict()
    #     isHeading = dict()
    #     for line_num in range(len(self.content)):
    #         for checkName in ["name",":"]:
    #             name.update(self.checkLine(checkName,name,self.content[line_num], line_num))
    #         for checkWork in ["work","experience"]:
    #             work_experience.update(self.checkLine(checkWork,work_experience, self.content[line_num],line_num))
    #         if line_num != len(self.content) - 1:
    #             if len(self.content[line_num + 1]) > len(self.content[line_num]):
    #                 isHeading.update(self.addValue(isHeading,line_num))
    #         if line_num > 0:
    #             if self.content[line_num - 1] == "":
    #                 isHeading.update(self.addValue(isHeading,line_num))
    #         if len(self.content[line_num]) == len(self.content[line_num].lstrip()):
    #             isHeading.update(self.addValue(isHeading,line_num))
    #         if self.content[line_num] == "":
    #             isHeading[line_num] = isHeading.get(line_num,0) - 1

    #     self.name = self.dict_List(name, self.content)
    #     self.work = self.dict_List(work_experience, self.content)
    #     self.headings = self.dict_List(isHeading, self.content)
    #     self.headings = [x[0] for x in self.headings]



    # def extract_experiences(self, string):
    #     experience = re.findall(r'\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}', string)
    #     days_in_year = 365.2425    
    #     exp = int((date.today('Dec 2020') - experience).days / days_in_year) 
    #     return experience      




    # def extract_skills(self,nlp_text, noun_chunks):
    #     '''
    #     Helper function to extract skills from spacy nlp text

    #     :param nlp_text: object of `spacy.tokens.doc.Doc`
    #     :param noun_chunks: noun chunks extracted from nlp text
    #     :return: list of skills extracted
    #     '''
    #     tokens = [token.text for token in nlp_text if not token.is_stop]
    #     data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    #     skills = list(data.columns.values)
    #     skillset = []
    #     # check for one-grams
    #     for token in tokens:
    #         if token.lower() in skills:
    #             skillset.append(token)
        
    #     # check for bi-grams and tri-grams
    #     for token in noun_chunks:
    #         token = token.text.lower().strip()
    #         if token in skills:
    #             skillset.append(token)
    #     return [i.capitalize() for i in set([i.lower() for i in skillset])]

    # def extract_experiences(self, string):
    #     # phonelist = None
    #     r = re.compile(r'(\d{0}[-\.\s]??\d{1}[-\.\s]??\d{1}|\(\d{0}\)\s*\d{1}[-\.\s]??\d{1}|\d{0}[-\.\s]??\d{1}[-\.\s]??\d{1})')
    #     experiences = r.findall(string)
    #     experience = [re.sub(r'\D', '', number) for number in experiences]
    #     return experience



if __name__ == "__main__":
    verose = False
    if "-v" in str(sys.argv):
        verose = True
    p = Parse(verose)
    print(p.information)
    # print (resume.get_name())
