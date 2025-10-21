import requests
import json

# prueba_a.py — Parte A (API HTTP con requests)
# Decision: uso 'requests' por su sencillez y manejo de errores HTTP integrado.

# 2) Constantes
# Decision: el endpoint correcto para chat en Ollama es /api/chat
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"
# 3) Mensajes (formato estilo chat)
messages = [
    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
]
# 4) Construcción del payload
payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False, # Decision: False = respuesta completa en un único JSON; más simple para acceder a 'message.content'.
    "options": {"temperature": 0.2} # Decision: temp baja para respuestas más deterministas.
}
# 5) Envío de la petición y manejo de errores
def main():
    try:
        # Decision: timeout para evitar bloqueos si el servidor no responde.
        resp = requests.post(OLLAMA_API, json=payload, headers=HEADERS,timeout=120)
        resp.raise_for_status() # Decision: lanza HTTPError si el status no es 2xx (200 OK)

        data = resp.json() # Decision: la API devuelve JSON.

        print(data["message"]["content"])# Decision: con stream=False, el texto vive en data["message"]["content"].

    except requests.exceptions.ConnectionError as e:
        # Error 1: servidor no disponible.
        print("[ERROR] No se pudo conectar con el servidor Ollama en http://localhost:11434")
        print("Verificar: 1) 'ollama serve' o app inicializada, 2) 'curl http://localhost:11434/api/tags'")
        print(e)
    except requests.exceptions.HTTPError as e:
        # Error HTTP no 2xx (404/500/400…).
        print("[ERROR] Respuesta HTTP no exitosa (¿404/500?). Revisa el endpoint y el payload.")
        print(f"Sugerencia: confirma el modelo con 'ollama pull {payload['model']}'.")
        print(e)
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        # Formato inesperado (p. ej., se activo stream=True por error o cambio la API).
        print("[ERROR] Formato JSON inesperado. Asegúrate de usar stream=False y el endpoint '/api/chat'.")
        print(e)
if __name__ == "__main__":
    main()