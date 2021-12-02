FROM python:3.8


COPY requirements.txt /app/

WORKDIR /app


RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
