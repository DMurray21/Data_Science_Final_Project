import pandas as pd
import os.path as osp
import json
import warnings
import argparse
import numpy as np
import nltk
import operator
from nltk.stem import WordNetLemmatizer 
stopwords = nltk.corpus.stopwords.words("english")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input',help="Path to the input data file.")
    args = parser.parse_args()
    posts = []
    codes = {}
    with open(args.input, "r") as fp:
        for line in fp:
            post=json.loads(line)
            posts += [post]

            code = post["code"]
            if not (code in codes): 
                codes[code]=[]
            codes[code] +=  [post]
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    lemmatizer = WordNetLemmatizer() 
    clean = {}
    for code in codes:
        group=codes[code]
        clean[code] = []
        for post in group:
            post = post["title"].lower()
            post = tokenizer.tokenize(post)
            for i in range(len(post)):
                post[i] = lemmatizer.lemmatize(post[i])
            clean[code] += [post]
    
    for code in clean:
        score = tf_idf(clean[code])
        print(f"The tf-idf scors for {code} topic: {score}")


def tf_idf(titles):
    words = [] 
    scores = {}
    for title in titles:
        for word in title:
            if not(word in words or word in stopwords):
                words += [word] 
    for word in words:
        tf=0
        df=0
        for title in titles:
            tf += (np.array(title)==word).sum()
            df += (word in title)
        scores[word] = np.log(tf/df)
    top = {}
    for i in range(10):
        key = max(scores.items(), key=operator.itemgetter(1))[0]
        top[key] = scores.pop(key)
    

    return top
            

if __name__ == "__main__":
    main()