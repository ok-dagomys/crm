FROM python:latest

COPY ./pyproject.toml /app
COPY .env /app
WORKDIR /app/tasks

RUN apt -y update
RUN apt -y full-upgrade
RUN apt -y dist-upgrade
RUN apt -y --purge autoremove
RUN apt -y autoclean

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENTRYPOINT ["python"]
CMD ["main.py"]