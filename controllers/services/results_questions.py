import pandas as pd

def save_new_questions(pregunta):
    # Crea un DataFrame con la pregunta
    df = pd.DataFrame({'Pregunta': [pregunta]})

    # Intenta cargar el archivo Excel existente o crea uno nuevo si no existe
    try:
        existing_df = pd.read_excel('../ChatBot/data/download_files/preguntas_nuevas.xlsx')
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    # Guarda el DataFrame actualizado en el archivo Excel
    updated_df.to_excel('../ChatBot/data/download_files/preguntas_nuevas.xlsx', index=False)
    


def save_review(review,respuesta,pregunta):
    df = pd.read_csv('../ChatBot/data/data.csv')
    fila = df[df['detalle'] == pregunta]
    if not fila.empty:
        # Obtiene el índice de la fila encontrada
        indice_fila = fila.index[0]

        # Actualiza la columna 'buena' o 'mala' según la revisión
        if review:
            df.at[indice_fila, 'buena'] = 'X'
        else:
            df.at[indice_fila, 'mala'] = 'X'

        # Guarda el DataFrame actualizado en el archivo CSV
        df.to_csv('../ChatBot/data/data.csv', index=False)
    #df.to_csv('../ChatBot/data/data.csv', index=False)