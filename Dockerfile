FROM python:3.8

WORKDIR /code

COPY /dash/requirements.txt .

RUN pip install -r requirements.txt

COPY / .

CMD ["python", "./dash/app.py"]