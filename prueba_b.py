# prueba_b.py — (SDK oficial 'ollama', sin requests)
# Decisión: el SDK simplifica la llamada y abstrae detalles HTTP/headers.
import ollama
import argparse # Decision: manejar --model y --outfile consistentemente con Parte A.
from datetime import datetime # Decision: timestamp para nombrar el archivo de salida.
import time # Decision: medir duración total de la operación.

MODEL = "llama3.2"
messages = [
    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
]
def parse_args():
    p = argparse.ArgumentParser(description="Invoca Ollama vía SDK de Python.")
    p.add_argument("--model", default=MODEL, help="Modelo a usar (por defecto: llama3.2)")
    p.add_argument("--outfile", default=None, help="Ruta de salida .txt (si no se indica, usa timestamp).")
    return p.parse_args()

def main():
    args = parse_args()
    t0 = time.perf_counter()  # Extra: medir duracion total.

    try:
        # Decision: ollama.chat es la funcion de alto nivel equivalente a POST /api/chat.
        response = ollama.chat(model=args.model, messages=messages)

        # Decision: la estructura de respuesta mantiene 'message' → 'content'.
        texto = response["message"]["content"]
        print(texto)

        # Extra: guardado con timestamp y modelo en el nombre por trazabilidad.
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outname = args.outfile or f"salida_prueba_b_{args.model}_{ts}.txt"
        with open(outname, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"[INFO] Guardado en: {outname}")

    except Exception as e:
        # Servidor parado o modelo inexistente.
        # 1) parar 'ollama serve' (ConnectionError del cliente interno),
        # 2) usar un modelo inexistente (error desde backend).
        print("[ERROR] Fallo la invocación vía SDK. Verifica 'ollama serve' y 'ollama pull' del modelo indicado.")
        print(e)
    finally:
        t1 = time.perf_counter()
        print(f"[INFO] Duración total: {t1 - t0:.2f}s")

if __name__ == "__main__":
    main()