FROM python:3.12-slim

WORKDIR /app

COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/ .

# Déplacer la DB seedée hors du répertoire de données (sera copiée au démarrage si absente)
RUN mv maturity.db /app/maturity.db.seed || true

EXPOSE 8000

# Au démarrage : copier la DB seed si le volume est vide, puis lancer gunicorn
CMD ["sh", "-c", "if [ ! -f /app/data/maturity.db ]; then mkdir -p /app/data && cp /app/maturity.db.seed /app/data/maturity.db 2>/dev/null; fi && gunicorn --bind 0.0.0.0:8000 --workers 2 app:app"]
