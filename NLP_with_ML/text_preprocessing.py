import spacy
import pandas as pd

nlp = spacy.load('en_core_web_sm')

def remove_lower(series):
    output  = series.str.lower()
    output = series.str.replace(r'\[.*?\]', '', regex=True)
    output =output.str.replace(r'[^\w\s]', '', regex=True)
    return output

def token_lemma_nonstop(text):
    doc= nlp(text)
    output = [token.lemma_ for token in doc if not token.is_stop]
    return ' '.join(output)

def clean_normalize(series):
    output = remove_lower(series)
    output = output.apply(token_lemma_nonstop)
    return output

# allow command line execution
if __name__ =="__main__":
    print('Text preprocessing module is ready to use')
