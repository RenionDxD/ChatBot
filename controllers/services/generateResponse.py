import openai
from openai import OpenAI
import json
import time
from controllers.services.check_history import rectificar_historial
# pip install openai
# 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

def core_gpt(prompt):
    time.sleep(5) 
    #try:
        #with open('../ChatBot/config/history.json', 'r') as file:
        #        config = json.load(file)
        #key = config['keyGPT']
        #client = OpenAI(api_key=key,)
        #reformula para entendimiento de usuario
        #response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        #messages=[{"role": "user", "content": prompt},])
        #response = response.choices[0].message.content
    #except Exception as e:
        #color_question = False
        #return f"Lamentamos los inconvenientes. ¡Por ahora, el chat no está disponible! ¡Pronto estaremos de vuelta!. :( Si este error persiste puedes comunicarte con nuestras operadoras"
    return prompt#response

def generate_prompt(text_solucion,redireccion,pregunta,comentario):
    context_pregunta = f"pregunta que genera respuesta: [{pregunta}]"
    summary = f'comentario: [{comentario}]'
    context = search_context(redireccion)
    solucion = f"[{text_solucion}]"
    prompt = f"{context}{solucion} : {context_pregunta} , {summary}"
    return prompt




def search_context(redireccion):
    rute = rectificar_historial()
    variables_y_valores = []
    with open(f'{rute[0]}/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, valor = linea.strip().split('=')
            variables_y_valores.append((variable.strip(), valor.strip()))

    for i in variables_y_valores:
        if redireccion == i[0]:
            context = i[1]

    
    return context