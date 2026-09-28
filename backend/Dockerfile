FROM python:3.11-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /src

WORKDIR /src


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && sed -i 's/\r$//' /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
