FROM python:3
WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/. .

CMD ["python3", "main.py"]
# EXPOSE 8000