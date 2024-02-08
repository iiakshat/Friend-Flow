FROM python:3.8-slim

WORKDIR /friend-flow

COPY . /friend-flow

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "App/app.py"]
