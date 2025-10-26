1) Pasos previos
	1.	Instalar/arrancar Ollama y descargar el modelo
      ollama serve                     
      ollama pull llama3.2
      curl http://localhost:11434/api/tag
 	2.	Crear proyecto en PyCharm con Virtualenv
  	•	PyCharm → New Project → Pure Python → New environment using Virtualenv.
  	•	Base interpreter: tu python3 (3.9+).
  	•	Create → Trust Project.
	3.	Instalar dependencias en el intérprete del proyecto
  	•	GUI: PyCharm → Preferences (⌘,) → Project → Python Interpreter → + → instala requests y ollama.
  	•	O Terminal en PyCharm:
    pip install --upgrade pip
    pip install requests ollama
2) Pasos — Parte A (API HTTP con requests)
	1.	Crear el archivo
	  •	Panel Project → clic derecho en la carpeta → New → Python File → prueba_a.py.
	2.	Pegar el código final (con comentarios de justificación por decisión técnica).
	3.	Configurar ejecución en PyCharm
    •	Run → Edit Configurations… → + (Python)
    •	Script path: ruta a prueba_a.py
    •	Working directory: carpeta del proyecto
    •	(Opcional) Parameters: --model phi3 --outfile salida_phi3.txt
    •	OK
	4.	Ejecutar
  	•	Botón Run (flecha verde) o ⌃R.
  	•	El texto de respuesta del modelo.
	5.	Errores frecuentes y verificación
  	•	ConnectionError: arranca Ollama (ollama serve) y prueba curl http://localhost:11434/api/tags.
  	•	HTTPError / modelo no disponible: ollama pull <modelo> y revisa que MODEL coincide.
  	•	KeyError/JSONDecodeError: asegúrate de stream=False y endpoint /api/chat.
	6.	Checklist Parte A
  	•	stream: false → respuesta en un JSON.
  	•	Texto en ["message"]["content"].
  	•	Éxito esperado: HTTP 200 OK.
--------------------------------------
3) Pasos — Parte B (SDK ollama, sin requests)
	1.	Crear el archivo
	  •	New → Python File → prueba_b.py.
	2.	Pegar el código final (con comentarios de justificación).
(Ya te lo proporcioné en el chat; pégalo íntegro en prueba_b.py.)
	3.	Configurar ejecución en PyCharm
  	•	Run → Edit Configurations… → + (Python)
  	•	Script path: prueba_b.py
  	•	Working directory: carpeta del proyecto
  	•	OK
	4.	Ejecutar
  	•	Run.
  	•	El texto de respuesta del SDK.
	5.	Errores frecuentes
  	•	Servidor parado o modelo inexistente → ollama serve y ollama pull <modelo>.
  	•	Si falta el paquete: pip install ollama en el mismo intérprete del proyecto.
--------------------------------------
4) Extras implementados (cómo usarlos)
  Los extras están en ambas partes 
A) Cambiar el modelo por línea de comandos (--model)
	•	Parte A (HTTP):
    python prueba_a.py --model phi3
  •	Parte B (SDK):
    python prueba_b.py --model phi3
B) Guardar la respuesta a .txt con timestamp (--outfile opcional)
	•	Si no pasas --outfile, se guardará con un nombre automático:
	•	salida_prueba_a_<modelo>_<YYYYmmdd_HHMMSS>.txt
	•	salida_prueba_b_<modelo>_<YYYYmmdd_HHMMSS>.txt
C) Medición de tiempo de inferencia
	•	Ambas partes imprimen al final:
  [INFO] Duración total: X.XXs  
