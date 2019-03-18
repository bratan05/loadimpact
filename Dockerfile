FROM python:3.6
ENV PYTHONBUFFERED 1
RUN mkdir /server
WORKDIR /server
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN python -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /server/
