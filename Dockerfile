FROM python:3.9 as builder

RUN python3.9 -m venv /usr/share/python3/app
ADD app/requirements.txt /tmp/
RUN pip install --no-cache-dir -Ur /tmp/requirements.txt && \
    python3 -m spacy download ru_core_news_md

FROM builder as app

ADD app /mnt/app/
ADD models /mnt/models/

WORKDIR /mnt/app

CMD ["python3", "app.py"]
