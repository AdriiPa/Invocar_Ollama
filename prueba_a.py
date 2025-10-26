# prueba_a.py — Parte A (API HTTP con requests) + extras CLI, guardado .txt y tiempo

import requests # Decision: librería HTTP de alto nivel para POST JSON.
import json     # Decision: para diagnosticar/parsing y capturar JSONDecodeError.
import argparse # Decision: manejar --model y --outfile de forma clara.
import time     # Decision: medir tiempo total de llamada (inferir latencia total).
from datetime import datetime # Decision: timestamp legible para el nombre del archivo.

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
def build_payload(model: str):
    # 4) Construcción del payload
    return {
        "model": model,
        "messages": messages,
        "stream": False,
        # Decision: False = respuesta completa en un único JSON; más simple para acceder a 'message.content'.
        "options": {"temperature": 0.2}  # Decision: temp baja para respuestas más deterministas.
    }

def parse_args():
    # Decision: argparse da UX clara y validación básica de argumentos.
    p = argparse.ArgumentParser(description="Invoca Ollama vía HTTP (requests).")
    p.add_argument("--model", default=MODEL, help="Modelo a usar (por defecto: llama3.2)")
    p.add_argument("--outfile", default=None, help="Ruta de salida .txt (si no se indica, usa timestamp).")
    return p.parse_args()


# 5) Envío de la petición y manejo de errores
def main():
    args = parse_args()
    payload= build_payload(args.model)

    t0=time.perf_counter() #Extra: medir duracion total de la llamada
    try:
        # Decision: timeout para evitar bloqueos si el servidor no responde.
        resp = requests.post(OLLAMA_API, json=payload, headers=HEADERS,timeout=120)
        resp.raise_for_status() # Decision: lanza HTTPError si el status no es 2xx (200 OK)

        data = resp.json() # Decision: la API devuelve JSON.

        # Decision: cuando el modelo no existe/no esta descargado, Ollama puede devolver {"error": "..."} con 200.
        if isinstance(data, dict) and "error" in data:
            raise  RuntimeError(f"Ollama informo de un error: {data['error']}")

        # Decisión: con stream=False, el texto vive en data["message"]["content"].
        texto= data["message"]["content"]
        print(texto)

        # Extra: guardado con marca temporal y modelo en el nombre.
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outname = args.outfile or f"salida_prueba_a_{args.model}_{ts}.txt"
        with open(outname, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"[INFO] Guardado en: {outname}")

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

    finally:
        t1=time.perf_counter()
        print(f"[INFO] Duracion total: {t1-t0:.2f} segundos.")
if __name__ == "__main__":
    main()