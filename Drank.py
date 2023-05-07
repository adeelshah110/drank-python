# Imports
import urllib
import nltk
import sys
import re 

import lxml
import math
import string
import textwrap
import requests

from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import defaultdict,Counter
from nltk.corpus import stopwords
from collections import defaultdict 
from bs4.element import Comment

from nltk import wordpunct_tokenize
from urllib.parse import urlparse 

import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

Common_Nouns ="january debt est dec big than who use jun jan feb mar apr may jul agust dec oct ".split(" ")
URL_CommnWords =['','https','www','com','-','php','pk','fi','http:','http']
URL_CommonQueryWords = ['','https','www','com','-','php','pk','fi','https:','http','http:']
UselessTagsText =['html','style', 'script', 'head',  '[document]','img']
def Scrapper1(element):
    if element.parent.name in [UselessTagsText]:
        return False
    if isinstance(element, Comment):
        return False
    return True

def Scrapper2(body):             
    soup = BeautifulSoup(body, 'lxml')      
    texts = soup.findAll(text=True)   
    name =soup.findAll(name=True) 
    visible_texts = filter(Scrapper1,texts)        
    return u" ".join(t.strip() for t in visible_texts)

def Scrapper3(text):                  
    lines = (line.strip() for line in text.splitlines())    
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return u'\n'.join(chunk for chunk in chunks if chunk)


def Scrapper_title_4(URL):
  req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()
  title=[]
  
  soup = BeautifulSoup(html, 'lxml') 
  title.append(soup.title.string)
  return(title,urls)

def Web_Funtion(URL):
  req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()  
  Raw_HTML_Soup = BeautifulSoup(html, 'lxml') 
 
  raw =Scrapper2(html)
  Raw_text = Scrapper3(raw) 
  return(Raw_text,Raw_HTML_Soup) 
#

def _calculate_languages_ratios(text):  
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]    
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
       
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) 
    return languages_ratios



def detect_language(text):
    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    stop_words_for_language = set(stopwords.words(most_rated_language))
    return most_rated_language,stop_words_for_language

def Preprocessing_Text(Raw_text, stop_words_for_language):
    
    # 1 making text as a space seperated word list
    stop_words_for_language = str(stop_words_for_language).lower()
    Words_in_text =[]
    for word in Raw_text.split():                    
        Words_in_text.append(word)

    
     #2 remove numbers and special charactes from words
        
    alphawords_only = [word for word in Words_in_text if word.isalpha()]          
    
    #3 removing length 1 words
    
    Words_afterRemoval_onelength = [word for word in alphawords_only if len(word)>1]

    #4 lower case all words
    
    lower_case_only = [word.lower() for word in Words_afterRemoval_onelength ]
    
    # Remove stopwords 
    
    stopwords_nltk = set(stopwords.words("English"))  
    words_withoutStopwords = [word for word in lower_case_only if word not in stopwords_nltk]
    if stop_words_for_language != "english":
        words_withoutStopwords = [word for word in words_withoutStopwords if word not in stop_words_for_language]
    
    #removing words from common nouns like thank, use, gift, close
    
    words_withoutCommonNouns = [word for word in words_withoutStopwords if word not in Common_Nouns ]
    
    #return list of preprocess words
    
    return (words_withoutCommonNouns)

#<hr class ="new3">
def Calc_words_frequency(Text_words):
    
    Sorted_WordCount_dict ={}  
    word_and_fr_list=[]
    Count_fr = Counter(Text_words)    
    
    for word,word_count in Count_fr.most_common():
        word_and_fr_list.append([word, word_count])
        Sorted_WordCount_dict[word]= word_count
        
    return(Sorted_WordCount_dict)
#<hr class ="new3">
#FEATURES 
#<hr class ="new3">
def Function_ParseURL(URL):
    URL =str(URL)
    host=[]
    obj=urlparse(URL)    
    name =(obj.hostname)
    if len(name)>0:
        for x in name.split('.'):
            if x.lower() not in URL_CommonQueryWords:
                host.append(x)
        else:
            host.append(name)
    path=[]
    host_part_URL =[]
          
    for url_parts in URL.split('/'):
        for url_part in url_parts.split('.'):            
            if (len(url_part)>0):
                for url_words in url_part.split('-'):
                    if url_words.lower() not in URL_CommnWords and url_words.lower() not in host: 
                        path.append(url_words.lower())
            else:
                path.append(url_parts)                
    return(host,path)
#<hr class ="new3">
def function_TexDic_Filter(Tag_TextDic):
    alt_words=[]
    if len(Tag_TextDic) > 0:
        for k,i in Tag_TextDic.items():    
   
            for x in i:
                word=[n for n in x.split(',')]
                for x in word:
                    words=[i for i in x.split() ]
                    for x in words:
                        alt_words.append(x)
        return(alt_words)
    else:
        return(alt_words)
    
def function_Tag_Text(Raw_HTML_Soup,Tag_name):
    TagTextList=[]  
    for text in Raw_HTML_Soup.find_all(Tag_name):
        tag_text = text.text.strip().lower()
        TagTextList.append(tag_text)
    return TagTextList   

def function_HeaderTitleAnchorText(Raw_HTML_Soup):    
    H1_TextList = function_Tag_Text(Raw_HTML_Soup,'h1')
    H2_TextList = function_Tag_Text(Raw_HTML_Soup,'h2')
    H3_TextList= function_Tag_Text(Raw_HTML_Soup,'h3')
    H4_TextList = function_Tag_Text(Raw_HTML_Soup,'h4')
    H5_TextList = function_Tag_Text(Raw_HTML_Soup,'h5')
    H6_TextList = function_Tag_Text(Raw_HTML_Soup,'h6')
    Title_TextList = function_Tag_Text(Raw_HTML_Soup,'title')
    Anchor_TextList = function_Tag_Text(Raw_HTML_Soup,'a')
    return (H1_TextList,H2_TextList,H3_TextList,H4_TextList,H5_TextList,H6_TextList,Title_TextList,Anchor_TextList)
    
    
def function_MakeDictTagText(Raw_HTML_Soup):
     
    (H1_TextList,H2_TextList,H3_TextList,H4_TextList,H5_TextList,H6_TextList,Title_TextList,Anchor_TextList) = function_HeaderTitleAnchorText(Raw_HTML_Soup)
        
    H1_TextDict = {}
    H2_TextDict = {}
    H1_TextDict = {}
    H3_TextDict = {}
    H4_TextDict = {}
    H5_TextDict = {}
    H6_TextDict= {}
    Title_TextDict = {}
    Anchor_TextDict = {}
        
    H1_TextDict["h1"] = H1_TextList
    H2_TextDict["h2"] = H2_TextList
    H3_TextDict["h3"] = H3_TextList
    H4_TextDict["h4"] = H4_TextList
    H5_TextDict["h5"] = H5_TextList
    H6_TextDict["h6"] = H6_TextList    
    Title_TextDict["title"] = Title_TextList
    Anchor_TextDict["a"] = Anchor_TextList
    
    H1_dic = function_TexDic_Filter(H1_TextDict)
    H2_dic = function_TexDic_Filter(H2_TextDict)
    H3_dic = function_TexDic_Filter(H3_TextDict)
    H4_dic = function_TexDic_Filter(H4_TextDict)
    H5_dic = function_TexDic_Filter(H5_TextDict)
    H6_dic = function_TexDic_Filter(H6_TextDict)
    Title_dic = function_TexDic_Filter(Title_TextDict)
    Anchor_dic = function_TexDic_Filter(Anchor_TextDict)
    
    return (H1_dic, H2_dic, H3_dic, H4_dic, H5_dic, H6_dic, Title_dic, Anchor_dic)
#<hr class ="new3">
def Feature_Score(candidate_word,feature_words,score):
    total_score=0
    score_single_time =0    
    for word_feature in feature_words:        
        if word_feature ==candidate_word:            
            #total_score+=score
            score_single_time = score                
    return(score_single_time)
           
def Tf_Score(fr,text_length):
    if text_length<50:
        tf_score =((fr/100)*50)
    else:
        tf_score=((fr/100)*20) 
    return (tf_score)   
# <hr class ="new3">
def function_word_Fr_TagName_ScoreDic(words_count_dic, text_length,Raw_HTML_Soup):
    wrd_fr_Tgs_Fnl_score =defaultdict()
    Word_Final_Score =defaultdict()
    Host_part_of_URL, Query_part_of_URL = Function_ParseURL(URL)
    #names of features 10
    Name_FeaturesList =np.array(['H1', 'H2', 'H3','H4', 'H5', 'H6','Title','Anchor','URL-H','URL-Q'])
    
    # Manual score for words
    Manual_Score_Each_Features =np.array([6, 5, 4,3, 2, 2, 6, 1,5,4])
    
    
    
    # Get all the words in features
    
    (H1_dic, H2_dic, H3_dic, H4_dic, H5_dic, H6_dic, Title_dic, Anchor_dic)= function_MakeDictTagText(Raw_HTML_Soup)
    featuresText_allDict_npArrayList = np.array([H1_dic, H2_dic, H3_dic, H4_dic, H5_dic, H6_dic, Title_dic, Anchor_dic, Host_part_of_URL, Query_part_of_URL])
   
    
    for word,fr in words_count_dic.items():
        tf_score = Tf_Score(fr,text_length)
        tag =[]
        name_tag =[]
               
        for word_inAll_Dic in range (len(featuresText_allDict_npArrayList)):
            if word in featuresText_allDict_npArrayList[word_inAll_Dic]:   
                tag.append(Manual_Score_Each_Features[word_inAll_Dic]) 
                name_tag.append(Name_FeaturesList[word_inAll_Dic])
        score= (sum(tag))
        score = score + tf_score
        Word_Final_Score[word] = score
        wrd_fr_Tgs_Fnl_score[word] = fr,name_tag,score
    return (wrd_fr_Tgs_Fnl_score, Word_Final_Score)
#<hr class ="new3">

def function_Drank_KeywordExtraction(URL):
    Raw_text, Raw_HTML_Soup = Web_Funtion(URL)
    most_rated_language,stop_words_for_language = detect_language(Raw_text)
    
    preprocess_TextWords = Preprocessing_Text(Raw_text, stop_words_for_language )
    text_length = len(preprocess_TextWords)
    words_count_dic = Calc_words_frequency(preprocess_TextWords)
    
        # Features
    
    
    
    H1_TextList, H2_TextList, H3_TextList, H4_TextList, H5_TextList, H6_TextList,Title_TextList,Anchor_TextList = function_HeaderTitleAnchorText(Raw_HTML_Soup)
    
    #Feature Header, Title, Anchor text, score dictionary
    
    (wrd_fr_Tgs_Fnl_score, Word_Final_Score) = function_word_Fr_TagName_ScoreDic(words_count_dic, text_length,Raw_HTML_Soup)   
   
    Keywords =[]
    sorted_word_score = Counter(Word_Final_Score)
    
    for word,score in sorted_word_score.most_common(10):
        Keywords.append(word)
    return Keywords   

if __name__ == "__main__":    
    URL ="http://bbc.com"
    Keywords = function_Drank_KeywordExtraction(URL)
    print (Keywords)