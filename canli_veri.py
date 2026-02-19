import os

from flask.cli import load_dotenv
import requests
import pandas as pd
import sqlalchemy
import urllib
import time
from datetime import datetime

# Gizli kasayı (.env) aç
load_dotenv()

# Şifreleri kasadan güvenli bir şekilde çek
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# SQL Server Ayarları
Server = r'.\SQLEXPRESS05'
Database = 'DogusStaj'
Driver = 'ODBC Driver 17 for SQL Server'
Tablo_Adi = 'Kripto_Fiyatlari'

# Alarm Seviyesi (Şu an BTC kaç paraysa, ondan biraz daha YÜKSEK bir sayı yaz ki hemen alarm versin, test edelim)
KRITIK_FIYAT_ALT_SINIR = 98000.0  # Örneğin BTC 96 binde ise, 98 binin altı diye hemen alarm çalar

# 2. YARDIMCI FONKSİYONLAR
def telegram_alarm_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Gönderim Hatası: {e}")

# SQL Bağlantısını Kur
conn_str = f'DRIVER={{{Driver}}};SERVER={Server};DATABASE={Database};Trusted_Connection=yes;'
quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')


# 3. ANA MOTOR (SONSUZ DÖNGÜ)
print("AKILLI KRİPTO BOTU BAŞLATILDI!")
telegram_alarm_gonder(" Kripto Botu Başlatıldı. Piyasalar izleniyor...")

for i in range(1, 11):  # Test için 10 kere dönsün yeter
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
        print(f"[{i}/10]  {tarih} - BTC: {fiyat} $ -> Veritabanına Yazıldı.")
        
        # ALARM KONTROLÜ (ZEKA BURADA)
        if fiyat < KRITIK_FIYAT_ALT_SINIR:
            alarm_mesaji = f" DİKKAT ŞEF! \nBitcoin çakılıyor!\nAnlık Fiyat: {fiyat} $\nZaman: {tarih}"
            telegram_alarm_gonder(alarm_mesaji)
            print("   -> Telegram Alarmı Gönderildi!")
            
        time.sleep(5)
        
    except Exception as e:
        print(f" Hata: {e}")
        time.sleep(5)

print(" Sistem Durdu.")
telegram_alarm_gonder(" Bot görevini tamamladı ve durdu.")