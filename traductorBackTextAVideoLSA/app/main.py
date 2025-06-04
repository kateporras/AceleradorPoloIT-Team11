from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uuid
import os

from app.traductor import procesar_texto_glosas, procesar_texto_videoLSA
from moviepy import VideoFileClip, concatenate_videoclips

app= FastAPI()

# permisos para el front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],#"http://localhost:<num>" va el dominio del front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

#esto es si el modelo de entrada es en json
class textInput(BaseModel):
    text: str

#endpoints de la api
# *endpoint que responde a solicitudes POST 
@app.post("/traducir")
def traducir_text_a_videoLSA(input_text:textInput):
    text=input_text.text.strip()#elimina espacios al final y al inicio del text

    if not text:
        raise HTTPException(status_code=400,detail="Texto Vacio")
    
    #Procesamos el texto a glosas
    glosas= procesar_texto_glosas(text)
    rutas_videos_glosas=procesar_texto_videoLSA(glosas)

    #validamos si no se encontro glosas
    if not rutas_videos_glosas:
        raise HTTPException(status_code=404, detail="No se encontraron la traduccion")

    #Armamos los clips para unirlos
    clips=[]
    for path in rutas_videos_glosas:
        if os.path.exists(path):
            clips.append(VideoFileClip(path))
        else:
            print(f"<!> video no encontrado: {path}")
    
    if not clips: 
        raise HTTPException(status_code=500, detail="<!> No se pudo cargar ningun video")

    #Combinar y guardar
    final_clip=concatenate_videoclips(clips)
    fileOutput_name=f"{uuid.uuid4()}.mp4" #esto me genera un nombre randon al archivo video de salida
    output_path=os.path.join("output",fileOutput_name)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


    #liberar memoria clips
    for clip in clips:
        clip.close()
    final_clip.close()

    #Devolver el video al front
    return FileResponse(output_path, media_type="video/mp4", filename=fileOutput_name)



        
