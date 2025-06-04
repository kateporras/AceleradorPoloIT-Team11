import pandas as pd
import spacy

modeloSpacy=spacy.load("es_core_news_sm")
# si quieron verlo iterativo colocar #%%
dataf_Videos=pd.read_csv("./data/LSA_V1.csv")

#print(archVideos.head())

def procesar_texto_glosas(texto:str):
    doc = modeloSpacy(texto)
    resultGlosas=[]

    for token in doc:
        if not token.is_space and not token.is_punct:
            resultGlosas.append(token.lemma_.upper())

    return resultGlosas

def procesar_texto_videoLSA(glosas):
    rutasVideo=[]
    glosasRegex="|".join(glosas)
    dataf_VideosFiltrados=dataf_Videos[dataf_Videos["descripcion"].str.contains(glosasRegex)]

    for itemVideo in dataf_VideosFiltrados['videoURL']:
        rutasVideo.append(itemVideo)

    return rutasVideo

