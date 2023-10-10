FROM python:3.10.11

WORKDIR /testplan-to-pdf

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY testplan-to-pdf.py ./testplan-to-pdf.py

CMD [ "python", "./testplan-to-pdf.py" ]
