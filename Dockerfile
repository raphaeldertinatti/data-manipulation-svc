FROM python:alpine3.19
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 5432
CMD ["python","connection.py"]


