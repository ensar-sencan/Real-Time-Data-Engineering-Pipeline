# 1. ZEMİN SABİTLEME: Sürpriz yaşamamak için Debian 12 (Bookworm) sürümünü kilitliyoruz!
FROM python:3.10-slim-bookworm

# 2. Konteynerin içindeki çalışma masamızı belirliyoruz
WORKDIR /app

# 3. SQL Server ile konuşabilmek için Linux (Debian 12) ODBC sürücülerini kuruyoruz
RUN apt-get update && apt-get install -y curl apt-transport-https gcc g++ unixodbc-dev gnupg \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# 4. Kütüphane listemizi kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm kodlarımızı (.env kasan dahil) konteynerin içine kopyalıyoruz
COPY . .

# 6. Motoru Ateşle! Konteyner çalıştığında otomatik olarak botu başlat
CMD ["python", "-u", "canli_veri.py"]