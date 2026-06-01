# 1. Start with a lightweight, official Python 3.9 image
FROM python:3.9-slim

# 2. Tell Docker to work out of this directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first.
# (Docker caches steps. If you don't change dependencies, it skips downloading them next time).
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your source code into the container
COPY . .

# 6. Expose the port that Uvicorn will run on
EXPOSE 8000

# 7. The command to start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]