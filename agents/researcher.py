import streamlit as st
import google.genai as genai

class ResearcherAgent:
    def __init__(self):
        """
        Agente encargado de investigar productos desde URLs.
        Extrae beneficios, ganchos (hooks) y características principales.
        """
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def is_ready(self):
        return self.client is not None

    def analyze_url(self, url: str) -> dict:
        """
        Lee el contenido de una URL y extrae información de marketing usando Gemini.
        """
        if not self.is_ready():
            return {"error": "Gemini not configured"}

        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer texto relevante (remover scripts y estilos)
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            # Limitar a los primeros 5000 caracteres para no exceder tokens
            return self.extract_marketing_data(text[:5000])
            
        except Exception as e:
            return {"error": str(e)}

    def extract_marketing_data(self, page_content: str) -> dict:
        """
        Toma el contenido crudo de una página y devuelve un JSON con:
        - nombre_producto
        - dolor_principal
        - beneficios (lista)
        - ganchos_sugeridos (lista)
        """
        prompt = f"""Eres un experto en investigación de mercado y copywriting. 
Analiza el siguiente contenido de una página de producto y extrae la información clave para crear videos de TikTok.

CONTENIDO DE LA PÁGINA:
{page_content[:5000]}

RESPONDE ÚNICAMENTE EN FORMATO JSON CON ESTA ESTRUCTURA:
{{
  "nombre_producto": "Nombre corto",
  "dolor_principal": "El mayor problema que resuelve",
  "beneficios": ["beneficio 1", "beneficio 2"],
  "ganchos_sugeridos": ["Gancho 1", "Gancho 2"],
  "precio_estimado": "$0.00"
}}
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            import json
            # Limpiar respuesta de Gemini si tiene backticks
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            return {"error": f"Error parsing page content: {str(e)}"}
