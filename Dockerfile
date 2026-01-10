FROM python:3.12-alpine
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN addgroup -S app && adduser -S app -G app \
    && mkdir -p /app/logs && chown -R app:app /app
USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
