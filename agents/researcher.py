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
        Soporta extracción avanzada para TikTok y sitios dinámicos.
        """
        if not self.is_ready():
            return {"error": "Gemini not configured"}

        try:
            import requests
            from bs4 import BeautifulSoup
            import json
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Búsqueda de DATOS ESTRUCTURADOS (TikTok / JSON-LD / Rehydration)
            extra_context = []
            
            # TikTok utiliza este ID específico para sus datos hidratados
            rehydration_data = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
            if rehydration_data and rehydration_data.string:
                extra_context.append(f"TIKTOK_DATA: {rehydration_data.string[:10000]}") # Limite generoso
            
            # Otros sitios usan JSON-LD
            json_ld = soup.find_all("script", type="application/ld+json")
            for ld in json_ld:
                if ld.string:
                    extra_context.append(f"JSON_LD: {ld.string}")

            # 2. Metadatos SEO
            meta_data = []
            for meta in soup.find_all("meta"):
                name = meta.get("name") or meta.get("property")
                content = meta.get("content")
                if name and content:
                    meta_data.append(f"{name}: {content}")
            
            meta_text = "\n".join(meta_data)

            # 3. Limpieza de texto del cuerpo
            for script in soup(["script", "style"]):
                script.decompose()
            body_text = soup.get_text(separator=' ', strip=True)
            
            # Construir contexto total para Gemini
            context_pieces = [
                "METADATA:\n" + meta_text,
                "STRUCTURED_DATA:\n" + "\n".join(extra_context),
                "BODY_TEXT:\n" + body_text
            ]
            combined_content = "\n\n".join(context_pieces)
            
            # Limitar a los primeros 12000 caracteres (Gemini 2.0 tiene ventana grande)
            return self.extract_marketing_data(combined_content[:12000])
            
        except Exception as e:
            return {"error": str(e)}

    def extract_marketing_data(self, combined_content: str) -> dict:
        """
        Toma el contenido crudo (Meta + Body) y devuelve un JSON de marketing.
        """
        prompt = f"""Eres un experto en investigación de mercado. Analiza este contenido de una página web.
        
TU OBJETIVO: Identificar de qué trata el producto o servicio real que se ofrece, ignorando la plataforma (TikTok/Amazon/Instagram).

REGLAS DE ORO:
1. Si los metadatos (METADATA) mencionan un perfil o descripción (ej: "Hidroponia en casa"), eso es lo que debes analizar.
2. No inventes beneficios de la red social. Busca el valor del CREADOR o PRODUCTO.
3. Si el contenido es 100% genérico sobre una red social y no hay ni rastro del producto, responde con un campo "error": "No se encontró información específica del producto en esta URL".

CONTENIDO A ANALIZAR:
{combined_content}

RESPONDE ÚNICAMENTE EN FORMATO JSON:
{{
  "nombre_producto": "Nombre real del producto/servicio/canal",
  "dolor_principal": "El problema exacto que resuelven (ej: falta de espacio para cultivar)",
  "beneficios": ["beneficio 1", "beneficio 2", "beneficio 3"],
  "ganchos_sugeridos": ["Gancho 1", "Gancho 2"],
  "precio_estimado": "Si se menciona, sino 'N/A'"
}}
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            import json
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # Validación de calidad básica
            if "TikTok" in data.get("nombre_producto", "") and len(combined_content) < 500:
                return {"error": "El scraper fue bloqueado o la página es dinámica. Por favor, describe el producto manualmente abajo."}
                
            return data
        except Exception as e:
            return {"error": f"Error al procesar el contenido: {str(e)}"}
