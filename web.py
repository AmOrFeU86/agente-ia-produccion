import gradio as gr
import requests
import os

# Coloca tu API key aquí o mejor como variable de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "TU_API_KEY_AQUI"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "gradio-chatbot"
}

def chat(message, history):
    """
    Función que maneja el chat con Gradio.
    history es una lista de tuplas [(user_msg, bot_msg), ...]
    """
    # Convertir el historial de Gradio al formato de OpenRouter
    conversation_history = []

    for user_msg, bot_msg in history:
        conversation_history.append({"role": "user", "content": user_msg})
        if bot_msg:
            conversation_history.append({"role": "assistant", "content": bot_msg})

    # Agregar el mensaje actual del usuario
    conversation_history.append({"role": "user", "content": message})

    # Llamar a la API
    data = {
        "model": "x-ai/grok-4.1-fast",
        "messages": conversation_history
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # Obtener la respuesta del asistente
        assistant_message = result["choices"][0]["message"]["content"]
        return assistant_message

    except Exception as e:
        return f"Error: {str(e)}"

# Crear la interfaz de Gradio
demo = gr.ChatInterface(
    fn=chat,
    title="Agente de IA con Memoria",
    description="Chatea con el asistente IA. Mantiene el contexto de la conversación.",
    examples=[
        "Hola, ¿cómo estás?",
        "¿Puedes ayudarme con Python?",
        "Explícame qué es machine learning"
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
