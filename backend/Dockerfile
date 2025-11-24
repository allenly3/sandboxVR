FROM python:3.12-slim
EXPOSE 8000
WORKDIR /
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic
COPY backend/server.py /server.py
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]