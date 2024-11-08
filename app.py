import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from faker import Faker

# Inicializar Faker para generar datos ficticios en español (Colombia)
fake = Faker('es_CO')

# Función para generar datos ficticios
def generate_fake_data(num_rows, selected_columns):
    data = {
        'Nombre': [fake.name() for _ in range(num_rows)],
        'Edad': np.random.randint(18, 70, size=num_rows),
        'Ciudad': [fake.city() for _ in range(num_rows)],
        'Email': [fake.email() for _ in range(num_rows)],
        'Teléfono': [fake.phone_number() for _ in range(num_rows)],
        'Fecha de Nacimiento': [fake.date_of_birth(minimum_age=18, maximum_age=70) for _ in range(num_rows)],
        'Salario': np.random.randint(30000, 120000, size=num_rows)
    }
    
    # Filtrar las columnas seleccionadas
    filtered_data = {col: data[col] for col in selected_columns}
    return pd.DataFrame(filtered_data)

# Diseño de la aplicación Streamlit
st.title("Generador de Datos Falsos")

# Opciones de columnas disponibles
available_columns = ['Nombre', 'Edad', 'Ciudad', 'Email', 'Teléfono', 'Fecha de Nacimiento', 'Salario']

# Selección de columnas por parte del usuario
selected_columns = st.multiselect("Selecciona las columnas que deseas incluir:", available_columns, default=available_columns)

num_rows = st.number_input("Número de filas a generar:", min_value=1, max_value=1000, value=10)

if st.button("Generar Datos"):
    # Generar los datos ficticios con las columnas seleccionadas
    df = generate_fake_data(num_rows, selected_columns)
    st.write(df)

    # Convertir el DataFrame a un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos Falsos')
        writer.save()
    
    # Preparar el botón de descarga para el archivo Excel
    output.seek(0)  # Mover al principio del buffer BytesIO
    st.download_button(
        label="Descargar archivo Excel",
        data=output,
        file_name='datos_falsos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )