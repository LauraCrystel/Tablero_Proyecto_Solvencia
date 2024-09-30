import streamlit as st
import pandas as pd
import plotly.express as px
import openai
#st.title("Dashboard de Solvencia Financiera")

st.markdown("<h1 style='text-align: center; color: white;'>Dashboard de Solvencia Financiera </h1>", unsafe_allow_html=True)

st.sidebar.header("Filtros")

url = "https://raw.githubusercontent.com/LauraCrystel/Tablero_Proyecto_Solvencia/refs/heads/main/Datos_proyecto_clean.csv"
data = pd.read_csv(url)


# Filtros interactivos
industria = st.sidebar.multiselect('Seleccionar Industria', options=data['Industry'].unique(), default=data['Industry'].unique())
pais = st.sidebar.multiselect('Seleccionar País', options=data['Country'].unique(), default=data['Country'].unique())
tamano_empresa = st.sidebar.multiselect('Seleccionar Tamaño de Empresa', options=data['Company_Size'].unique(), default=data['Company_Size'].unique())

st.sidebar.header("Caracteristicas")

opciones = ['Industria', 'País', 'Tamaño']
seleccion = st.sidebar.selectbox("Selecciona el desgloce de las gráficas:", opciones)

if seleccion == 'Id Compañia':
    seleccion2 = 'Company_ID' 
elif seleccion =="Industria":
    seleccion2 = 'Industry'
elif seleccion == "País":
    seleccion2 = 'Country'
elif seleccion == "Tamaño":
    seleccion2 = 'Company_Size'

# Filtrar datos
data_filtered = data[(data['Industry'].isin(industria)) & 
                     (data['Country'].isin(pais)) & 
                     (data['Company_Size'].isin(tamano_empresa))]



#Ajustes de los datos
# Calcular ratios financieros
total_capital = data_filtered['Equity'].sum()
total_revenue = data_filtered['Total_Revenue'].sum()
total_debt = data_filtered['Short_Term_Debt'].sum() + data_filtered['Long_Term_Debt'].sum()
total_c_assets = data_filtered['Current_Assets'].sum()
total_c_liabilities = data_filtered['Current_Liabilities'].sum()
total_f_expenses = data_filtered['Financial_Expenses'].sum()

total_current_ratio = total_c_assets / total_c_liabilities
total_debt_to_equity_ratio = total_debt / total_capital
total_interest_cov_ratio = total_revenue / total_f_expenses

df_agrupado = data_filtered.groupby(seleccion2).agg({
'Equity' : 'sum', 
'Total_Revenue' : 'sum',
'Short_Term_Debt' : 'sum',
'Long_Term_Debt' : 'sum', 
'Current_Assets' : 'sum', 
'Current_Liabilities' : 'sum',
'Financial_Expenses' : 'sum'}).reset_index()

df_agrupado['total_debt'] = df_agrupado['Short_Term_Debt'] + df_agrupado['Long_Term_Debt']

df_agrupado['Current_Ratio'] = df_agrupado['Current_Assets'] / df_agrupado['Current_Liabilities']
df_agrupado['Debt_to_Equity_Ratio'] = df_agrupado['total_debt'] / df_agrupado['Equity']
df_agrupado['Interest_Coverage_Ratio'] = df_agrupado['Total_Revenue'] / df_agrupado['Financial_Expenses']

st.markdown("<h3 style='text-align: center; color: white; font-size: 26px; font-weight: bold;'>Indicadores Financieros Totales de la Selección</h3>", unsafe_allow_html=True)


st.write("--------------------------------------------")

def fm(value):
    return f"{value / 1_000_000_000:,.2f}MM" if value >= 1_000_000_000 else str(value)

#KPIS generales

st.markdown("""
    <style>
    .header-text {
        font-size: 22px;
        color: lightblue;
        font-weight: bold;
        text-align: center;
    }
    .value-text {
        font-size: 20px;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Crear tres columnas
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.markdown('<p class="header-text">Capital</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p class="header-text">Ganancias</p>', unsafe_allow_html=True)
with col3:
    st.markdown('<p class="header-text">Deudas totales</p>', unsafe_allow_html=True)
with col4:
    st.markdown('<p class="header-text">Activos Corrientes</p>', unsafe_allow_html=True)

# Crear la segunda fila con valores
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.markdown(f'<p class="value-text">{fm(total_capital)}</p>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<p class="value-text">{fm(total_revenue)}</p>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<p class="value-text">{fm(total_debt)}</p>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<p class="value-text">{fm(total_c_assets)}</p>', unsafe_allow_html=True)

st.write('')
st.write('')
st.write('')

st.markdown(f"<h3 style='text-align: center; color: violet; font-size: 20px; font-weight: bold;'>Por {seleccion}</h3>", unsafe_allow_html=True)

fig01 = px.pie(df_agrupado, names=seleccion2, values='Equity', color_discrete_sequence=px.colors.sequential.Blues_r)
fig01.update_layout( title={
        'text': f"Capital",
        'font': {'size': 18},  # Tamaño del título
        'x': 0.5,  # Centrar el título
        'xanchor': 'center'
    }
)
fig01.update_layout(
    width=600,  # Ancho en píxeles
    height=400  # Alto en píxeles
)

fig02 = px.scatter(
    df_agrupado,
    x='Long_Term_Debt',
    y='Short_Term_Debt',
    size='total_debt',
    color=seleccion2,
    hover_name=seleccion2,  # Muestra la categoría al pasar el mouse
    size_max=60,  # Tamaño máximo de las burbujas
    color_discrete_sequence=px.colors.sequential.Greens_r,
              labels={"Long_Term_Debt": "Deuda a Largo Plazo", "Short_Term_Debt": "Deuda a Corto Plazo"})
fig02.update_layout( title={
        'text': f"Deuda",
        'font': {'size': 18},  # Tamaño del título
        'x': 0.5,  # Centrar el título
        'xanchor': 'center'
    }
)
fig02.update_layout(
    width=600,  # Ancho en píxeles
    height=400  # Alto en píxeles
)

col1, col2 = st.columns([1,2])

with col1:
    st.plotly_chart(fig01)
with col2:
    st.plotly_chart(fig02)

st.write("")

# Mostrar ratios financieros
st.markdown("<h3 style='text-align: center; color: white; font-size: 26px; font-weight: bold;'>Ratios Financieros</h3>", unsafe_allow_html=True)

st.write("--------------------------------------------")

# CSS para centrar el texto y darle formato personalizado
st.markdown("""
    <style>
    .header-text {
        font-size: 22px;
        color: lightblue;
        font-weight: bold;
        text-align: center;
    }
    .value-text {
        font-size: 20px;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Crear tres columnas
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<p class="header-text">Liquidez Total</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p class="header-text">Deuda a Patrimonio</p>', unsafe_allow_html=True)
with col3:
    st.markdown('<p class="header-text">Cobertura de Gastos</p>', unsafe_allow_html=True)

# Crear la segunda fila con valores
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f'<p class="value-text">{round(total_current_ratio, 5)}</p>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<p class="value-text">{round(total_debt_to_equity_ratio, 5)}</p>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<p class="value-text">{round(total_interest_cov_ratio, 5)}</p>', unsafe_allow_html=True)

st.write('')

fig1 = px.bar(df_agrupado, x = seleccion2, y='Current_Ratio', color = 'Current_Ratio', color_continuous_scale = 'Blues',
              labels={"Current_Ratio": "Ratio de Liquidez", seleccion2: seleccion})
fig1.update_layout( title={
        'text': f"Ratio de Liquidez por {seleccion}",
        'font': {'size': 24},  # Tamaño del título
        'x': 0.5,  # Centrar el título
        'xanchor': 'center'
    }
)
st.plotly_chart(fig1)


fig2 = px.bar(df_agrupado, x = seleccion2, y='Debt_to_Equity_Ratio', color = 'Debt_to_Equity_Ratio', 
              color_continuous_scale = 'Greens',
              labels={"Debt_to_Equity_Ratio": "Deuda a Patrimonio", seleccion2: seleccion})
fig2.update_layout( title={
        'text': f"Ratio de Deuda a Patrimonio por {seleccion}",
        'font': {'size': 24},  # Tamaño del título
        'x': 0.5,  # Centrar el título
        'xanchor': 'center'
    }
)
st.plotly_chart(fig2)

fig3 = px.bar(df_agrupado, x = seleccion2, y='Interest_Coverage_Ratio', color = 'Interest_Coverage_Ratio', 
              color_continuous_scale = 'Cividis',
              labels={"Interest_Coverage_Ratio": "Cobertura de Gastos Financieros", seleccion2: seleccion})
fig3.update_layout( title={
        'text': f"Cobertura de Gastos Financieros por {seleccion}",
        'font': {'size': 24},  # Tamaño del título
        'x': 0.5,  # Centrar el título
        'xanchor': 'center'
    }
)
st.plotly_chart(fig3)



# Análisis de estadísticas
st.markdown("<h3 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>Estadísticas Descriptivas de los Ratios</h3>", unsafe_allow_html=True)


df_stats = data_filtered[['Current_Ratio', 'Debt_to_Equity_Ratio', 'Interest_Coverage_Ratio']].describe()
df_stats = df_stats.rename(columns = {"Current_Ratio": "Ratio de Liquidez",
                                      "Debt_to_Equity_Ratio": "Deuda a Patrimonio",
                                      "Interest_Coverage_Ratio": "Cobertura de Gastos Financieros"})
df_stats2 = df_stats.style \
    .set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#E84855'), ('color', 'white'), ('font-weight', 'bold')]}
    ])
st.markdown(df_stats2.to_html(), unsafe_allow_html=True)

st.write("--------------------------------------------")

client = openai.OpenAI(api_key=openai_api_key)

def obtener_respuesta(prompt):
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
      messages=[
          {"role": "system", "content": """
          Eres experto en el área de solvencia,
          entonces vas a responder todo desde la perspectiva financiera. Contesta siempre en español
          en un máximo de 50 palabras, utiliza un lenguaje que sea entendible para todo público.
          """}, #Solo podemos personalizar la parte de content
          {"role": "user", "content": prompt}
      ]
  )
  output = response.choices[0].message.content
  return output

prompt_user= st.text_area("Pregunta al asistente virtual: ")

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)

#Mostrar los filtros
st.write('Los datos contienen información de estas selecciones:')
st.write('Industrias: ' + ', '.join(industria))
st.write('Paises: ' + ', '.join(pais))
st.write('Tamaños: ' + ', '.join(tamano_empresa))

st.write("Creado por: **Laura Crystel Carreño Olivera** :ghost:") 
