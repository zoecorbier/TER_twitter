import pandas as pd #1.1.4
import spacy #3.0.5
import plotly_express as px #0.4.1
import plotly.io as plt # 4.14.3
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv('emotion.csv', sep=';')

def emotion_phrase(phrase):
    liste_emotion = []
    phrase = nlp(phrase)
    for token in phrase:
        mot = token.text
        for i in range(len(df)):
            if(df.loc[i, 'English (en)'] == mot):
                liste_emotion.append(df.loc[i,:].tolist())
    #Retourne une colonne avec les emotions par mot dans le phrase
    return pd.DataFrame(liste_emotion, columns=['English (en)', 'Positive' ,'Negative','Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust'])

def emotion_graph(text):
    # Récupére le resultat
    result_emotion = emotion_phrase(text)
    # Régule la dateframe avec certain column
    df=result_emotion[['English (en)','Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']]
    #Mets en forme la dataframe
    new_df=pd.melt(df,id_vars="English (en)",value_vars=list(df.columns[1:]),var_name="Emotion")
    #Enlève les emotion qui ne sont pas présentent
    without_0=new_df[new_df["value"]!=0].iloc[:,:-1]
    #Créer le diagramme
    fig = px.parallel_categories(without_0,labels={'English (en)':'Word'})
    #Retourne le html
    return plt.to_html(fig)

if __name__ == "__main__":
    tweet="Job seeking can be incredibly stressful.\n\nIt can make you feel lost.\n\nHurt.\n\nAlone.\n\nNeed I say, depressed.\n\nMany o… https://t.co/XOVbx4fJFQ"
    emotion_graph(tweet)