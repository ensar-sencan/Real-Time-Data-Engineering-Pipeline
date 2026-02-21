import os

from dotenv import load_dotenv
import requests
import pandas as pd
import sqlalchemy
import urllib
import time
from datetime import datetime

#.env aç
load_dotenv()

# Şifreleri kasadan güvenli bir şekilde çek
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

## SQL Server Ayarları
Server = r'host.docker.internal,1433'  # Docker içinden SQL Server'a bağlanmak için özel adres ve port
Database = 'DogusStaj'
Driver = 'ODBC Driver 18 for SQL Server'

Tablo_Adi = 'Kripto_Fiyatlari'


# GÜVENLİ BAĞLANTI CÜMLESİ: Trusted_Connection sildik, yerine UID ve PWD koyduk!
conn_str = f'DRIVER={{{Driver}}};SERVER={Server};DATABASE={Database};UID={DB_USER};PWD={DB_PASS};TrustServerCertificate=yes;'
# Alarm Seviyesi (Şu an BTC kaç paraysa, ondan biraz daha YÜKSEK bir sayı yaz ki hemen alarm versin, test edelim)
KRITIK_FIYAT_ALT_SINIR = 98000.0  # Örneğin BTC 96 binde ise, 98 binin altı diye hemen alarm çalar

# 2. YARDIMCI FONKSİYONLAR
def telegram_alarm_gonder(mesaj):
    """Telegram'a anlık bildirim gönderen fonksiyon."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        response = requests.post(url, data=payload)
        # Eğer Telegram mesajı kabul etmezse (200 OK demezse), bize nedenini söylesin!
        if response.status_code != 200:
            print(f"TELEGRAM REDDETTİ: {response.text}")
    except Exception as e:
        print(f"SİSTEM HATASI: {e}")

# SQL Bağlantısını Kur
conn_str = f'DRIVER={{{Driver}}};SERVER={Server};DATABASE={Database};UID={DB_USER};PWD={DB_PASS};TrustServerCertificate=yes;'
quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')

# 3. ANA MOTOR (SONSUZ DÖNGÜ)
print("AKILLI KRİPTO BOTU BAŞLATILDI!")
telegram_alarm_gonder(" Kripto Botu Başlatıldı. Piyasalar izleniyor...")

sayac = 1
while True:  
    try:
        # Veriyi Çek
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url)
        veri = response.json()
        
        fiyat = float(veri['price'])
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # SQL'e Kaydet
        df = pd.DataFrame([{'Sembol': veri['symbol'], 'Fiyat': fiyat, 'Tarih': tarih}])
        df.to_sql(Tablo_Adi, con=engine, if_exists='append', index=False)
        print(f"[{sayac}]  {tarih} - BTC: {fiyat} $ -> Veritabanına Yazıldı.")
        
        #  ALARM KONTROLÜ
        if fiyat < KRITIK_FIYAT_ALT_SINIR:
            alarm_mesaji = f" DİKKAT ŞEF! \nBitcoin çakılıyor!\nAnlık Fiyat: {fiyat} $\nZaman: {tarih}"
            telegram_alarm_gonder(alarm_mesaji)
            print("   -> Telegram Alarmı Gönderildi!")
            
        time.sleep(5)
        sayac += 1 # Sayacı her adımda 1 artır
        
    except Exception as e:
        print(f"Hata: {e}")
        time.sleep(5)

print(" Sistem Durdu.")
telegram_alarm_gonder(" Bot görevini tamamladı ve durdu.")
