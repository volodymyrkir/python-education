FROM python:3.10

WORKDIR /data_engineering
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY script.py ./
EXPOSE 5000
CMD ["python","script.py"]