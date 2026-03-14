FROM python:3.11

RUN mkdir switches
WORKDIR  /switches


COPY pyproject.toml /switches/

RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install 

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "8080"]