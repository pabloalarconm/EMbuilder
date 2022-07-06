FROM python:3.8 
#3.9

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "embuilder.main:app"]
# "--host", "127.0.0.1", "--port", "8000"

ENTRYPOINT ["python3","embuilder/api_test.py"]

