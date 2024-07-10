FROM python:3.10-slim

WORKDIR /bsers/client

COPY ./client/.dist /bsers/client/

EXPOSE 5500

CMD ["python", "-m", "http.server", "5500"]
