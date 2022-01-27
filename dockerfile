FROM python

WORKDIR /Flangsbot

COPY ./requirements.txt /Flangsbot

ENV PYTHONUNBUFERED 1

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "launcher.py"]