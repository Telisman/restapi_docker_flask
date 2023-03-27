FROM python:3.8
ENV PYTHONUNUBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
CMD ["python", "app.py"]