from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from presentationProjet.lda.lda import LDA
from presentationProjet.feeling.feeling import EMOTION
lda = LDA()
emo = EMOTION()


def receivetweet(resquest):
    if resquest.method == "POST":
        tw = resquest.POST.get('tweet')
        score, word = analysisLDA(tweet = tw)
        fee = analysisEmotion(tweet = tw)
        di = {"score":score, "word":word.tolist(), "fee":fee}
        return JsonResponse(di)

def analysisLDA(tweet = "Job seeking can be incredibly stressful.\n\nIt can make you feel lost.\n\nHurt.\n\nAlone.\n\nNeed I say, depressed.\n\nMany o… https://t.co/XOVbx4fJFQ"):
    return lda.predict_topic(text = tweet, return_words=True)

def analysisEmotion(tweet = ""):
    return emo.emotion_graph(tweet)
    



def etude1 (resquest):
    return render(resquest, "Exemple_Etude/exemple.html") 

def detailLDA (resquest):
    return render(resquest, "Exemple_Etude/dlaVis_T8.html") 
