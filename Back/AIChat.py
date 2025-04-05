# ai.py
import openai
from config import OPENAI_API_KEY

# Initialize OpenAI client
openai_client = openai.Client(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)

def generate_recomendations(chat_context, question):
    prompt = f"""
Eres un asistente para negocios que recomendaras estrategias comerciales, logisticas o de marketing segun la información proporcionada

### Buisness Context
{buisness_context}	
### Chat Context
{chat_context}
### User Request
<user_request> {question} </user_request>
### Tarea:
- Generar una respuesta como asistente para ayudar el negocio
"""
    try:
        completion = openai_client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Tu eres un asistente útil que genera ideas creativas para ayudar a los negocios."},
                {"role": "user", "content": prompt},
            ]
        )
        

        if completion is None:
            raise ValueError("API retorno none, intenta de nuevo")
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generated: {e}")
        return "No se pudo generar una respuesta. Por favor intente de nuevo."
    

buisness_context = """
Nuestro negocio es un restaurante de comida rápida, nuestra especialidad son las hamburguesas.
Nuestro publico objetivo son estudiantes universitarios, manejamos precios bajos entre 18 mil pesos a 25 mil pesos
El día más frecuente es el viernes y sabado donde estas personas vienen a comer antes o después de salirnde fiesta.
"""

    
