from django.shortcuts import render
from django.http import HttpResponse

from presentationProjet.lda.lda import LDA
lda = LDA()


def etude1 (resquest):
    print("hey")
    mytext = "issue at school cant talk to mum and dad"
    prob_scores, words_topic, = LDA.predict_topic(text = mytext, return_words=True)
    return render(resquest, "Exemple_Etude/exemple.html") 