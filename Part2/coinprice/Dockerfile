FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x run_server.sh
EXPOSE 8000
CMD ["sh","run_server.sh"]