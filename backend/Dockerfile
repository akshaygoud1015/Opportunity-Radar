FROM python:3.12-slim

WORKDIR /app

# tectonic is distributed as a static binary -- no texlive install needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates libssl-dev libfontconfig1 \
    && curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
    && mv tectonic /usr/local/bin/tectonic \
    && apt-get purge -y curl && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
