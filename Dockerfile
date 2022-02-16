FROM python:3.8.12 as base

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base as runtime

COPY --from=base /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV PYTHONPATH="/home/atmuser/app/subclasses/"


RUN useradd --create-home atmuser
WORKDIR /home/atmuser
USER atmuser

COPY app/source ./app/
ENTRYPOINT ["python", "app/main.py"]

