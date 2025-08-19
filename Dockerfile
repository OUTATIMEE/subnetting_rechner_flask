# 1. Basis-Image wählen (Python 3.12 auf einem kleinen Linux)
FROM python:3.12-slim

# 2. Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# 3. Abhängigkeiten ins Image kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Restlichen Code ins Image kopieren
COPY . .

# 5. Port im Container öffnen (Flask läuft auf 8000)
EXPOSE 8000

# 6. Startbefehl für den Container
CMD ["python", "app.py"]
