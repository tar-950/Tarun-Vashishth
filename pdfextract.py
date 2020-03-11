import PyPDF2
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import io

# def pdfextract(file):
#     fileReaderObj = open(file, 'rb')
#     fileReader = PyPDF2.PdfFileReader(fileReaderObj)
#     countpage = fileReader.getNumPages()
#     count = 0
#     text = []
#     while count < countpage:    
#         pageObj = fileReader.getPage(count)
#         count +=1
#         t = pageObj.extractText()
#         text.append(t)
#     fileReaderObj.close()

#     print(text)
#     return text

def pdfextract(path):
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