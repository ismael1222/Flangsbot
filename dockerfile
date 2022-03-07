FROM python:slim

LABEL manteiner="Flangrys @flangrys"
LABEL build_date="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

WORKDIR /Flangsbot
COPY . .

# RUN apt-get update && \
#     apt-get -y install gcc mono-mcs && \
#     rm -rf /var/lib/apt/lists/*

RUN python -m pip install pip --upgrade
RUN python -m pip install -r requirements.txt
CMD ["python", "launcher.py"]