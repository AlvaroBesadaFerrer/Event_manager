import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv()

if "GEMINI_API_KEY" not in os.environ:  # Verifica si la variable de entorno está creada
    st.error("GEMINI_API_KEY not found in environment")
    st.stop()
# Tiene que definir la variable de entorno GEMINI_API_KEY con su clave de API de Google GenAI, instrucciones en el README.


from google import genai

client = genai.Client()

st.title("Agregar evento con IA")

prompt = st.text_input("Describe el evento")

if st.button("Generar con IA") and prompt:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    st.write(response.text)


# TODOOOOOOOOOO
# Agregar al req y readme
# python-dotenv
# google-genai
# streamlit
# .env file with GEMINI_API_KEY
