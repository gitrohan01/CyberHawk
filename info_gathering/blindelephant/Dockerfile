FROM python:3.11-slim

RUN pip install blindelephant

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/blindelephant

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
