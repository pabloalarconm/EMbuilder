FROM python:3.8 
#3.9

WORKDIR /code

COPY ./embuilder /code/embuilder
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "embuilder.main:app"]