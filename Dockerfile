FROM python:3.13.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SAIGONBITE_DATABASE=/data/saigonbite.db

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 10001 --create-home --shell /usr/sbin/nologin saigonbite \
    && mkdir -p /data && chown 10001:10001 /data
COPY . .
RUN chmod +x docker-entrypoint.sh
USER 10001:10001
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--workers", "2", "--threads", "4", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
