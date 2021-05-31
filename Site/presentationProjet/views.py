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
        anaLDA = analysisLDA(tweet = tw)
        if len(anaLDA)>1: 
            di = {"score":anaLDA[0], "word":anaLDA[1].to_frame().to_html()}
        else:
            di = {"score":anaLDA}
        fee = analysisEmotion(tweet = tw)
        di["fee"]=fee
        return JsonResponse(di)

def analysisLDA(tweet = "Job seeking can be incredibly stressful.\n\nIt can make you feel lost.\n\nHurt.\n\nAlone.\n\nNeed I say, depressed.\n\nMany o… https://t.co/XOVbx4fJFQ"):
    return lda.predict_topic(text = tweet, return_words=True)

def analysisEmotion(tweet = ""):
    return emo.emotion_graph(tweet)
    



def etude1 (resquest):
    return render(resquest, "Exemple_Etude/exemple.html") 

def detailLDA (resquest):
    return render(resquest, "Exemple_Etude/dlaVis_T8.html") 
