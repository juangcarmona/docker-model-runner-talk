FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Python deps (cache-friendly)
COPY openai_web_client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code as a package
COPY openai_web_client/ ./openai_web_client/

# Non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8081 5680

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8081/health').read()" || exit 1

CMD ["python", "-m", "openai_web_client.main"]
