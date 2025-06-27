# Exemple : users/Dockerfile
#FROM python:3.11

FROM djassa-auth-proxy

#WORKDIR /app
RUN rm -rf /app
WORKDIR /app
COPY . .
RUN pip install hvac

#RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
