FROM 3.10.13-bullseye

# Prevent pyc files from being copied to the container
ENV PYTHONDONTWRITEBYTECODE 1

#Ensure python output is logged in the container's terminal
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Copy the file 'requirements.txt' from the local build context to the container's file system.
COPY ./requirements.txt /requirements.txt

# Install python dependencies without cached packeges
RUN pip install -r /requirements.txt --no-cache-dir


# Set the working directory
WORKDIR /app

# Run Uvicorn to start your Python web application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]