FROM python:3.10

RUN mkdir app
COPY .env /app
COPY cfg.py /app
COPY pyproject.toml /app
WORKDIR /app/src/bot

RUN apt -y update
RUN apt -y full-upgrade
RUN apt -y dist-upgrade
RUN apt -y --purge autoremove
RUN apt -y autoclean

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENV PYTHONPATH /app
ENTRYPOINT ["python"]
CMD ["main.py"]