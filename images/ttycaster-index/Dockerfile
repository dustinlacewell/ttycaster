FROM python:2

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ADD ./index.py /index.py
ADD ./index.html /static/index.html
ADD ./index.css /static/index.css

ENTRYPOINT ["python", "/index.py"]
