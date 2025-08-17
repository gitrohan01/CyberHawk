FROM node:20-slim

RUN npm install -g wappalyzer

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/wappalyzer

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
