FROM python:2

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ADD ./index.py /index.py

ENTRYPOINT ["python", "/index.py"]
