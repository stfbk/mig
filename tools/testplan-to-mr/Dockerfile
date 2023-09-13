FROM python:3.10.11

WORKDIR /testplan-to-mr

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY testplan-to-mr.py ./testplan-to-mr.py

CMD [ "python", "./testplan-to-mr.py" ]
