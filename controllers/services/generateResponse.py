import openai
from openai import OpenAI
import time
# pip install openai
# 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

def core_gpt(text_solucion,redireccion,pregunta):
    context_pregunta = "pregunta que genera respuesta: " + "["+pregunta+"]"
    context = search_context(redireccion)
    solucion = "["+text_solucion+"]"
    prompt = context + solucion+" : "+context_pregunta
    time.sleep(2)
    #try:
        #client = OpenAI(api_key="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",)    
        #reformula para entendimiento de usuario
        #response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        #messages=[{"role": "user", "content": prompt},])
        #response = response.choices[0].message.content
    #except:
        #return "Lamentamos los inconvenientes. ¡Por ahora, el chat no está disponible! ¡Pronto estaremos de vuelta!."
    return prompt#response




def search_context(redireccion):
    variables_y_valores = []
    with open('../ChatBot/data/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, valor = linea.strip().split('=')
            variables_y_valores.append((variable.strip(), valor.strip()))

    for i in variables_y_valores:
        if redireccion == i[0]:
            context = i[1]

    
    return context