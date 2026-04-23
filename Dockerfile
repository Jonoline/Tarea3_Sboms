FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash appuser

RUN pip install --break-system-packages semgrep

RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

RUN syft --version && grype --version && semgrep --version

WORKDIR /app

COPY pipeline/requirements.txt .
RUN pip install --break-system-packages -r requirements.txt

COPY pipeline/src/ ./src/

RUN mkdir -p data/raw/repos

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]