FROM python:3.11-slim
WORKDIR /app
COPY connection.py .
COPY init.sql /app/
COPY dataset/ ./dataset/

RUN pip install psycopg2-binary
RUN pip install pandas 
RUN pip install sqlalchemy

EXPOSE 5432

CMD ["python","connection.py"]


