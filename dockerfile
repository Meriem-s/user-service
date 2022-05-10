FROM python:3.9.7
COPY ./app /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
