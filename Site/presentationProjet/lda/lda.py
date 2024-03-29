# pip install skl2onnx


import pickle
import pandas as pd
import numpy as np
import spacy
import re
import plotly.express as px
import plotly

import os

import matplotlib.pyplot as plt 

import spacy

import pyLDAvis
import pyLDAvis.sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import joblib

class LDA():

    def __init__(self) -> None:
        self.vectorizer = joblib.load("./presentationProjet/lda/lda_vectorizer")
        self.model =  joblib.load("./presentationProjet/lda/lda_model")
        self.nlp = self._prepare_nlp()
        self.lemmatizer = self.nlp.get_pipe("lemmatizer")
        self.topicnames = ["Topic" + str(self._map_on_pyldavis_topinames(i)) for i in range(8)]
        self.df_topic_keywords = self._prepare_df_topic_keywords()

    def _map_on_pyldavis_topinames(self, value):
        mapper = dict(zip(np.arange(8),["Social(-)","Famille(n)","Liberation(+)","Communication(-)","Passage-a-l'acte(-)","Colère(-)","Social(+)","Problèmes(n)"],))
        return mapper[value]
    




    def predict_topic(self, text: str, return_words=False):
        """ 
        Parameters
        -----------
            text:  String, text to compute the topic distribution from
            return_words:   Boolean, return or not the words found in the text that has been used to compute topic distribution as pd.Series(columns = words, values= importance of word in topic)
        Return
            tupple: dictionary of topics_names and score
        -------

        """
        doc = self.nlp(text)
        # Step : Clean and Lemmatize
        text_clean = " ".join([w.lemma_ for w in self.lemmatizer(doc) if self._clean_text(w)])
        # Step 3: Vectorize transform
        text_vec = self.vectorizer.transform([text_clean])
        # Step 4: LDA Transform
        topic_distribution_scores = self.model.transform(text_vec).squeeze()
        dict_topic_distribution_scores = dict(zip(self.topicnames, topic_distribution_scores))

        num_topic = self._map_on_pyldavis_topinames(np.argmax(topic_distribution_scores))
        #words_topic = self.df_topic_keywords.loc["Topic{}".format(num_topic), self.df_topic_keywords.columns.intersection(text_clean.split(" "))]
        words_topic = self.df_topic_keywords.loc[:, self.df_topic_keywords.columns.intersection(text_clean.split(" "))]
        fig_words = px.line(words_topic.T)
        fig_words.update_xaxes(title_text='termes')
        fig_words.update_yaxes(title_text='% du terme dans le topic')
        if return_words:
            return  pd.Series(dict_topic_distribution_scores).to_frame().to_html(), plotly.io.to_html(fig_words)
            # return pd.Series(dict_topic_distribution_scores).to_frame(), fig_words
        else:
            return pd.Series(dict_topic_distribution_scores).to_frame().to_html()

    def _prepare_nlp(self):
        nlp = spacy.load("en_core_web_sm")
        words = ["na","rid","nd","bc","rn","ve","nt","www"]
        for w in words:
            nlp.vocab[w].is_stop = True
        return nlp
            

    # remove token with digits inside
    def _hasNumbers(self, inputString):
        return bool(re.search(r'\d', inputString))
        
    def _clean_text(self, token):
        """ Input should be spacy token object"""
        return  not token.is_stop and not token.like_num and not self._hasNumbers(token.text)


    # Define function to predict topic for a given text document.

    # # Show top n keywords for each topic
    # def show_topics_kwords(self):
    #     keywords = np.array(self.vectorizer.get_feature_names())
    #     topic_keywords = []
    #     for topic_weights in self.model.components_:
    #         top_keyword_locs = (-topic_weights).argsort()
    #         topic_keywords.append(keywords.take(top_keyword_locs))
    #     return topic_keywords

    def _prepare_df_topic_keywords(self):
        df_topic_keywords = pd.DataFrame(self.model.components_ / self.model.components_.sum(axis=1)[:, np.newaxis]) ##### Problème ici : 
        # Assign Column and Index
        df_topic_keywords.columns = self.vectorizer.get_feature_names()
        df_topic_keywords.index = self.topicnames
        return df_topic_keywords



if __name__ == "__main__":

    # Predict the topic
    lda = LDA()
    mytext = "Job seeking can be incredibly stressful. It can make you feel lost. Hurt. Alone. Need I say, depressed. Many of us, including me, have been there. It’s not easy. But, it’s not permanent, either. I came across something that I wanted to share"
    prob_scores, fig_words, = lda.predict_topic(text = mytext, return_words=True)

    # fig_words = px.line(words_topic.T, x="words", y="relevance", color='topics')

    # print(words_topic.T)
    # fig_words = px.line(words_topic.T)
    # fig_words.show()

    print(prob_scores)
    # Example output:
    # fuck    160.911980
    # kill     28.588706
    # life     29.083978
    # want      1.302537
    # Name: Topic5, dtype: float64
    # [0.02504828 0.02500956 0.025      0.02505407 0.02503615 0.51149085
    #  0.33832289 0.0250382 ]