# Wybór bazowego obrazu
FROM python:3.9-alpine
# Ustawienie katalogu roboczego
WORKDIR /app
# Przekopiowanie kodu python, wymaganych zależności oraz skryptu wait-for do kontenera
COPY code /app/
COPY requirements.txt /app/requirements.txt
COPY wait-for.sh /app/wait-for.sh
# Dodanie użytkownika oraz nadanie mu uprawnień (w celu zwiększenia bezpieczeństwa skrypt nie będzie uruchamiany z uprawnieniami root) oraz zainstalowanie potrzebnych zależności (psycopg2 - biblioteka umożliwiająca w Pythonie nawiązywania sesji z bazą Postgresową)
RUN adduser -D appuser && chown -R appuser /app && pip install --no-cache-dir -r /app/requirements.txt && chmod +x /app/wait-for.sh
# Przełączenie się na użytkownika
USER appuser
# Ustawienie domyślnego procesu po starcie kontenera - skryptu pythona
ENTRYPOINT ["/app/wait-for.sh", "python", "/app/script.py"]
# Wykorzystanie CMD jako domyślnego parametru dla ENTRYPOINT
CMD ["Kinga"]