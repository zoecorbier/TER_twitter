from django.shortcuts import render
from django.http import HttpResponse

from presentationProjet.lda.lda import LDA
from presentationProjet.feeling.feeling import EMOTION
lda = LDA()
emo = EMOTION()


def etude1 (resquest):

    tweet="Job seeking can be incredibly stressful.\n\nIt can make you feel lost.\n\nHurt.\n\nAlone.\n\nNeed I say, depressed.\n\nMany o… https://t.co/XOVbx4fJFQ"
    print(emo.emotion_graph(tweet))

    return render(resquest, "Exemple_Etude/exemple.html") 

def analysis():
    mytext = "issue at school cant talk to mum and dad"
    prob_scores, words_topic = lda.predict_topic(text = mytext, return_words=True)
    
    