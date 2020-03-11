import re
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
import PyPDF2
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import io
from datetime import datetime


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


str = pdfextract(r'C:\Users\TarunVashishth\Desktop\aditya bhartia.pdf')
all = re.findall(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4})", str)
all.sort(key = lambda date: datetime.strptime(date, '%b %Y'))
start_date = datetime.strptime("01 {0}".format(all[0]), "%d %b %Y")
# print(start_date)
today_date = date.today()

exp_c = relativedelta(today_date, start_date)
# relativedelta(years=+2, months=+9, days=+12)
exp = exp_c
print(exp)

# def experience(dates):
#     i=0  
#     while i<len(dates):
#         start_date = datetime.strptime("01 {0}".format(dates[i]), "%d %b %Y")
#         end_date = datetime.strptime("01 {0}".format(dates[i+1]), "%d %b %Y")
#         print(end_date - start_date)
#         i+=2

# experience(all)
  

# mylist= sorted(all, reverse= True)
# print(mylist)

# doj1 = date(2010, 5, 12)  # First DOJ
# left1 = date(2012, 8, 8) # Left
# doj2 = date(2012, 9, 1) # Rejoin
# left2 = date(2014, 11, 19) # Left Again
# doj_c = date(12 , all[0]) # Rejoin Again
# today_date = date.today()
# exp1 = relativedelta(doj1, left1)
# exp1
# relativedelta(years=-2, months=-2, days=-27)
# exp1 = relativedelta(left1, doj1)
# exp2 = relativedelta(left2, doj2)
# exp_c = relativedelta(today_date, doj_c)
# exp1
# relativedelta(years=+2, months=+2, days=+27)
# exp2
# relativedelta(years=+2, months=+2, days=+18)
# exp_c
# relativedelta(years=+2, months=+9, days=+12)
# exp = exp_c
# exp
# relativedelta(years=+7, months=+1, days=+57)
# exp_tuple = (exp.years, exp.months, exp.days)
# print (exp)