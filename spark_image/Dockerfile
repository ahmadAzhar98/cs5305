FROM apache/spark:4.0.1-java21

# Define Versions
ENV SPARK_VERSION=4.0.1 \
    DELTA_VERSION=4.0.1 \
    PYTHON_VERSION=3.14 \
    SCALA_VERSION=2.13 \
    HOME=/home/spark \
    PYSPARK_PYTHON=python3 \
    SPARK_MODE=MASTER \
    SPARK_HOME=/opt/spark

USER root

RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev \
        python${PYTHON_VERSION}-venv \
        vim \
        wget \
        netcat-openbsd \
        net-tools \
        iputils-ping && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install uv
    
# Install Delta Lake Python Bindings
RUN uv pip install --system \
    delta-spark==${DELTA_VERSION} \
    pyspark==${SPARK_VERSION} \
    pyspark[pipelines] \
    grpcio \
    protobuf \
    jupyterlab

# Download Delta Lake JARs directly to Spark jars directory
RUN cd /opt/spark/jars && \
    wget https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/io/delta/delta-connect-server_${SCALA_VERSION}/${DELTA_VERSION}/delta-connect-server_${SCALA_VERSION}-${DELTA_VERSION}.jar && \
    chown spark:spark *.jar

# Setup directories, permissions, and entrypoint script
RUN mkdir -p /opt/spark/startup /home/spark && \
    chown -R spark:spark /opt/spark /home/spark && \
    usermod -d /home/spark spark

COPY ./entrypoint.sh /opt/spark/startup/entrypoint.sh
RUN chmod +x /opt/spark/startup/entrypoint.sh

EXPOSE 9999

ENTRYPOINT ["/opt/spark/startup/entrypoint.sh"]