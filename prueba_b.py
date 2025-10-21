# prueba_b.py — (SDK oficial 'ollama', sin requests)
# Decisión: el SDK simplifica la llamada y abstrae detalles HTTP/headers.
import ollama
MODEL = "llama3.2"
messages = [
    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
]
try:
    # Decision: ollama.chat es la contraparte de POST /api/chat en el SDK
    response = ollama.chat(model=MODEL, messages=messages)
    # Decision: la estructura de respuesta mantiene 'message' → 'content'.
    print(response["message"]["content"])
except Exception as e:
    # Manejo minimo: servidor parado o modelo no descargado.
    # Como reproducirlo: 1) parar 'ollama serve', 2) usar un modelo inexistente.
    print("[ERROR] Fallo la invocacion vía SDK. Verifica 'ollama serve' y 'ollama pull llama3.2'.")
    print(e)