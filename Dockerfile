FROM python:3.10
ENV PYTHONNUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY . .
RUN pip install -r ./requirements.txt
RUN pip install requests