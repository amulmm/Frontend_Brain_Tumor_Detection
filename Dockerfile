FROM python:3.9-slim

WORKDIR /app

COPY requirements_backend.txt .
RUN pip install --no-cache-dir -r requirements_backend.txt

COPY . .

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "api_backend:app"]