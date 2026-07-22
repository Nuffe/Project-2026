FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "run.py"]