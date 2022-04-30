import pickle
import re
from datetime import datetime
from threading import Thread
from nltk.tokenize import word_tokenize, sent_tokenize


import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from tika import parser
import tika

def get_features(document):
    
    word_features = pickle.load(open('models/word_features.pickle', 'rb'))
    words = set(word_tokenize(str(document)))
    words = [word_lower.lower() for word_lower in words]
    features = {}
    for word in word_features:
        features[word] = word in words
    return features

#parse and classify text
def parser_pdf_docx(pdf_file):
    tika.initVM()
    result = {}
    experience = []
    education = []
    skills = []
    
    with open('models/NBclassifier.pickle', 'rb') as f:
        model = pickle.load(f)
    
    raw = parser.from_file(pdf_file)

    for text in sent_tokenize(raw['content']):
        if text != '':
            catg = model.classify(get_features(text))
            
            if catg == 'experience':
                experience.append(text.lower())
            if catg == 'education':
                education.append(text.lower())
            if catg == 'skills':
                skills.append(text.lower())
                
    result['experience'] = ' '.join(experience).lower()
    result['education'] = ' '.join(education).lower()
    result['skills'] = ' '.join(skills).lower()

    return result


#parse and classify text
def parser_text(text_content):
    # text_content = text_content.replace(r"<.+>","")
    # text_content = text_content.replace(r"</.+>","")
    import re
    # print("text_content ----------------->: ",text_content)

    text_content = re.sub(
            '<[a-z]+[0-9]*\s*(\s+[a-zA-Z]+=".+")?>|<\/([a-z]|[0-9])+>', 
            "", 
            text_content
    )
    print("text_content ----------------->: ",text_content)
    
    result = {}
    experience = []
    education = []
    skills = []
    
    with open('models/NBclassifier.pickle', 'rb') as f:
        model = pickle.load(f)

    for text in sent_tokenize(text_content):
        if text != '':
            catg = model.classify(get_features(text))
            if catg == 'experience':
                experience.append(text)
            if catg == 'education':
                education.append(text)
            if catg == 'skills':
                skills.append(text)
                
    result['experience'] = ' '.join(experience).lower()
    result['education'] = ' '.join(education).lower()
    result['skills'] = ' '.join(skills).lower()

    return result


def cleaning_text(text):
    text_result = ""
    text_tokenize = word_tokenize(text)
    for uplet in nltk.pos_tag(text_tokenize): 
        if uplet[1] =="NN" or uplet[1] == "NNP":
            text_result+= " " + uplet[0]
    return text_result


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def create_dataframe(matrix, tokens):
    doc_names = [f'doc_{i+1}' for i, _ in enumerate(matrix)]
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    return(df)


def cosinus_sim(data):
    if not data[0] and not data[1]:
        return 1.0
    
    if data[0] and data[1]:
        # Tfidf_vect = TfidfVectorizer()
        # vector_matrix = Tfidf_vect.fit_transform(instance_data)
        # tokens = Tfidf_vect.get_feature_names()

        count_vectorizer = CountVectorizer()
        vector_matrix = count_vectorizer.fit_transform(data)
        tokens = count_vectorizer.get_feature_names()
        
        create_dataframe(vector_matrix.toarray(),tokens)    
        cosine_similarity_matrix = cosine_similarity(vector_matrix)
        df_sim = create_dataframe(cosine_similarity_matrix, ['doc_1','data_2'] )
        
        print(df_sim)
        
        return df_sim['doc_1']['doc_2']

    return 0.0





def extract_education(sentence):
    r = {}
    result = sent_tokenize(sentence)
    with open('models/education.pickle', 'rb') as f:
        education = pickle.load(f)
    educations = []
    degrees = []
    for degree in education.items():
        for d in degree[1]:
            for educ in result:
                if educ.find(d + ' ') != -1:
                    educations.append(educ)
                    degrees.append(degree[0])
                    break
    r['education'] = list(set(educations))
    r['degree'] = list(set(degrees))
    return r


