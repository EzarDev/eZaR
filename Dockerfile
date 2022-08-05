FROM python:3.10-slim-buster

WORKDIR /bot

RUN pip install poetry

RUN apt update && apt install git -y && apt clean

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["task", "start"]
