# Step 1: Use a Python base image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install system dependencies (optional)
RUN apt-get update && apt-get install -y curl build-essential

# Step 4: Install Poetry dependency manager
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy poetry configuration files to install dependencies
COPY pyproject.toml poetry.lock /app/

# Step 7: Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Step 8: Copy the rest of the project files
COPY . /app/

# Step 9: Expose port 5500 (custom set for Flask)
EXPOSE 5500

# Step 10: Run the Flask application using Poetry
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]