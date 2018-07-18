FROM oculomotor-base:latest

ADD ./application /application

ENV PYTHONPATH /application

EXPOSE 80

CMD ["python", "/application/server.py"]
