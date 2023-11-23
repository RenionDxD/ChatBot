import pandas as pd


def save_new_questions(pregunta):
    # Crea un DataFrame con la pregunta
    df = pd.DataFrame({'Pregunta': [pregunta]})

    # Intenta cargar el archivo Excel existente o crea uno nuevo si no existe
    try:
        existing_df = pd.read_excel('tu_archivo.xlsx')
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    # Guarda el DataFrame actualizado en el archivo Excel
    updated_df.to_excel('tu_archivo.xlsx', index=False)