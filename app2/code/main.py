from flask import Flask, render_template, url_for,request
import re
import pandas as pd
import spacy
from spacy import displacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import en_core_web_md
import es_core_news_md


def get_lang_detector(nlp, name):
    return LanguageDetector()

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
    

@app.route('/process', methods = ['POST'])
def process():

    nlp = spacy.load("en_core_web_md")
    text = request.form['rawtext']
    opt = request.form['taskoption']
    Language.factory("language_detector", func=get_lang_detector)
    # document level language detection. Think of it like average language of the document!
    nlp.add_pipe('language_detector', last=True)    
    doc = nlp(text)
    #print(doc._.language)
    results_lang = doc._.language['language']
    if results_lang == 'es':
        nlp = spacy.load("es_core_news_md")


    results = []
    for ent in doc.ents:
        #t.append((ent.label_,ent.text))
        if opt == 'organization' and ent.label_ == 'ORG':
            results.append(ent.text)
        if opt == 'person' and ent.label_ == 'PERSON':
            results.append(ent.text)
        if opt == 'country' and ent.label_ == 'GPE':
            results.append(ent.text)
        if opt == 'location' and ent.label_ == 'LOC':
            results.append(ent.text)
        if opt == 'money' and ent.label_ == 'MONEY':
            results.append(ent.text)                                    
    num_of_results = len(results)

    return render_template('index.html',results=results,num_of_results=num_of_results,results_lang=results_lang)



if __name__ == '__main__':
    app.run(debug = True)
    