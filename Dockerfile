FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install -r requirements.txt
COPY ./config ./config/
COPY ./model/ ./model/
COPY ./repositories/ ./repositories/
COPY ./router/ ./router/
COPY ./schema/ ./schema/
COPY ./security ./security/
COPY ./services/ ./services/
COPY ./test/ ./test/
COPY app.py .
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]