FROM python:3.10-slim-bullseye

# Node.js, git və digər asılılıqları əlavə et
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "BrandrdXMusic"]
