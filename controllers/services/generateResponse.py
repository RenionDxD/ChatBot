import openai
from openai.api_resources import engine
# pip install openai


def core_gpt(text_solucion,redireccion,pregunta):
    context_pregunta = "pregunta que genera respuesta: " + "["+pregunta+"]"
    context = search_context(redireccion)
    solucion = "["+text_solucion+"]"
    prompt = context + solucion+" : "+context_pregunta
    #openai.api_key = "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"
    #reformula para entendimiento de usuario
    #completion = openai.Completion.create(engine="text-davinci-003",
    #                     prompt=prompt,
    #                    max_tokens=2048 )
    #response = completion.choices[0].text
    return prompt#response




def search_context(redireccion):
    
    # Crear una lista para almacenar las variables y valores
    variables_y_valores = []

    # Abrir el archivo en modo lectura
    with open('../ChatBot/data/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, valor = linea.strip().split('=')
            # Almacenar como una tupla (variable, valor)
            variables_y_valores.append((variable.strip(), valor.strip()))
            print(variable)
    if isinstance(redireccion, str) and redireccion == "usuario":
        context = variables_y_valores[0][1]+" "
    elif isinstance(redireccion, str) and redireccion == "soporte":
        context = variables_y_valores[1][1]+" "
    elif isinstance(redireccion, str) and redireccion == "codigo":
        context = variables_y_valores[2][1]+" "
    else:
        context = variables_y_valores[3][1]+" "
    
    return context