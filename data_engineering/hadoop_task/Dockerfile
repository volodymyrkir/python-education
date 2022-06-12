FROM bde2020/spark-base:3.1.1-hadoop3.2

ENV ENABLE_INIT_DAEMON false

ENV YARN_CONF_DIR=/etc/hadoop
ENV PYSPARK_PYTHON=python3

COPY requirements.txt /app/
RUN cd /app \
     && pip3 install -r requirements.txt

COPY app.py /app
COPY yarn-site.xml /etc/hadoop/

CMD ["/bin/bash", "/spark/bin/spark-submit", "--master=yarn", "--deploy-mode=client", "/app/app.py"]