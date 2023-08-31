# Dockerfile, Image, Container
FROM python:3.8

ADD . / ./

RUN pip install pandas steam

CMD ["python","./dash/scripts/refresh_data.py"]


