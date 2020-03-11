import csv
import re
def extract_skills(resume_string):
    # resume_string1 = resume_string
    resume_string = resume_string.replace(',',' ')
    #Converting all the charachters in lower case
    resume_string= resume_string.lower()

    with open(r"C:\Users\TarunVashishth\Desktop\resume-parser-master (1)\resume-parser-master\skills.csv", 'rt') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        your_list = your_list[0]
        your_list = [word.lower() for word in your_list]

    #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
    s = set(your_list)
    list_matched = []
    for item in s:
        if item in resume_string:
            list_matched.append(item)

    print(list_matched)

# import pandas as pd
# import spacy

# # load pre-trained model
# nlp = spacy.load('en_core_web_sm')
# # noun_chunks = nlp.noun_chunks

# def extract_skills(resume_text):
#     nlp_text = nlp(resume_text)

#     # removing stop words and implementing word tokenization
#     tokens = [token.text for token in nlp_text if not token.is_stop]
    
#     # reading the csv file
#     data = pd.read_csv(r"C:\Users\TarunVashishth\Desktop\resume-parser-master (1)\skill.csv") 
    
#     # extract values
#     skills = list(data.columns.values)
    
#     skillset = []
    
#     # check for one-grams (example: python)
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
    
#     # check for bi-grams and tri-grams (example: machine learning)
#     # for token in noun_chunks:
#     #     token = token.text.lower().strip()
#     #     if token in skills:
#     #         skillset.append(token)
    
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]