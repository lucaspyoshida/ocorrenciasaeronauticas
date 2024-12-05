import streamlit as st
import pandas as pd
from app import gerar_resposta

# Configurações iniciais da página
st.set_page_config(
    page_title="Análise de Ocorrências Aeronáuticas",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilo adicional (opcional) para deixar a interface mais elegante
st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to bottom, #f0f2f6, #ffffff);
        padding: 2rem;
    }
    .main > div {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.05);
    }
    .stTextInput > label, .stTextArea > label, .stButton > button {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stMarkdown h1, .stMarkdown h2 {
        font-family: Arial, sans-serif;
    }
    .stMarkdown h1 {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stMarkdown h2 {
        font-size: 1.8rem;
        font-weight: bold;
        color: #444444;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stMarkdown p {
        font-size: 1rem;
        line-height: 1.5;
        color: #555555;
    }
    .stButton button {
        background: #0066cc;
        color: #ffffff;
        border-radius: 5px;
        border: none;
        font-size: 1.1rem;
        padding: 0.6rem 1.2rem;
        cursor: pointer;
    }
    .stButton button:hover {
        background: #005bb5;
    }
    </style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("Análise de Ocorrências Aeronáuticas")
st.markdown("""
Esta aplicação permite analisar um texto descrevendo uma ocorrência aeronáutica e 
retornar as probabilidades de cada categoria de evento.

**Como usar:**
1. Cole ou digite o texto da ocorrência no campo abaixo.
2. Clique em **"Calcular Probabilidades"**.
3. Aguarde alguns instantes para ver o resultado, que mostrará as probabilidades e demais informações.
""")

# Lendo o conteúdo do arquivo
try:
    with open('ocorrencia.txt', 'r', encoding='utf-8') as arquivo:
        texto_inicial = arquivo.read()
except FileNotFoundError:
    texto_inicial = ""

# Campo de texto para entrada da ocorrência
texto_entrada = st.text_area(
    "Cole ou digite o texto da ocorrência aérea:",
    value=texto_inicial,  # Definindo o valor inicial
    height=200,
    placeholder="Exemplo: O avião apresentou problemas técnicos durante a decolagem, mas conseguiu retornar ao aeroporto sem incidentes."
)

# Botão para calcular as probabilidades
if st.button("Calcular Probabilidades"):
    if not texto_entrada.strip():
        st.warning("Por favor, insira o texto da ocorrência antes de continuar.")
    else:
        with st.spinner("Analisando o texto..."):
            try:
                resultado = gerar_resposta(texto_entrada)
                
                if resultado is None:
                    st.error("Não foi possível obter uma resposta válida. Tente novamente ou verifique as configurações.")
                else:
                    # Convertendo a string para dicionário usando eval()
                    valores = eval(resultado)

                    # Criando um dicionário apenas com as probabilidades
                    probabilidades = {
                        'Acidente': valores['acidente'],
                        'Incidente Grave': valores['incidente_grave'],
                        'Incidente': valores['incidente'],
                        'Ocorrência de Solo': valores['ocorrencia_solo'],
                        'Não Ocorrência': valores['nao_ocorrencia']
                    }
                    
                    # Criando o DataFrame e ordenando por probabilidade em ordem decrescente
                    df_prob = pd.DataFrame.from_dict(probabilidades, orient="index", columns=["Probabilidade (%)"])
                    df_prob = df_prob.sort_values(by="Probabilidade (%)", ascending=False)
                    
                    # Formatando os números para remover zeros desnecessários
                    df_prob["Probabilidade (%)"] = df_prob["Probabilidade (%)"].apply(lambda x: f"{x:g}")
                    
                    # Aplicando estilo para centralizar e colocar em negrito
                    df_prob_styled = df_prob.style.set_properties(**{
                        'text-align': 'center'
                    }).set_table_styles([
                        {'selector': 'td', 'props': [('text-align', 'center'), ('font-weight', 'bold')]}
                    ])
                    
                    st.subheader("Resultados")
                    st.markdown("### Probabilidades por categoria")
                    st.table(df_prob_styled)

                    st.metric("Incerteza", f"{valores['taxa_incerteza']}%")

                    # Exibindo o resumo e justificativa
                    st.markdown("### Resumo da Ocorrência")
                    st.write(valores['ocorrência'])
                    
                    st.markdown("### Justificativa")
                    st.write(valores['justificativa'])

                        
            except Exception as e:
                st.error(f"Erro ao processar a resposta: {str(e)}")
                st.error(f"Resposta recebida: {resultado}")  # Para debug
