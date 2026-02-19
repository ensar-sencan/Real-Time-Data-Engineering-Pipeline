import pandas as pd
import sqlalchemy
import urllib
import sys 

print(" ETL Süreci Başlatılıyor...\n")

# --- 1. ADIM: AYARLAR (Config) ---
DOSYA_ADI = 'yeni_personel.csv'
SERVER_ADI = r'.\SQLEXPRESS05' 
VERITABANI = 'DogusStaj'


try:
    # --- 2. ADIM: EXTRACT (Dosyayı Oku) ---
    print(f" '{DOSYA_ADI}' dosyası aranıyor...")
    df = pd.read_csv(DOSYA_ADI)
    print(f" Dosya bulundu! Toplam {len(df)} satır veri var.")
    
    # --- 3. ADIM: TRANSFORM (Veriyi Temizle) ---
    print("\n Veri temizliği yapılıyor...")
    
    # Kural 1: Yaşı 18'den küçükleri ele
    df_temiz = df[df['Yas'] >= 18].copy()
    
    # Kural 2: Maaşı 0 veya eksi olanları ele
    df_temiz = df_temiz[df_temiz['Maas'] > 0]
    
    # Kural 3: Yeni Prim Sütunu Ekle (%15)
    df_temiz['Prim'] = df_temiz['Maas'] * 0.15
    
    print(f" Temizlik bitti. {len(df) - len(df_temiz)} adet hatalı kayıt elendi.")
    print(df_temiz)

    # --- 4. ADIM: LOAD (Veritabanına Bas) ---
    print("\n🔌 Veritabanına bağlanılıyor...")
    
    # Bağlantı Ayarları
    Driver = 'ODBC Driver 17 for SQL Server'
    conn_str = f'DRIVER={{{Driver}}};SERVER={SERVER_ADI};DATABASE={VERITABANI};Trusted_Connection=yes;'
    quoted_conn_str = urllib.parse.quote_plus(conn_str)
    engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')
    
    # SQL'e Yazma
    TABLO_ADI = 'Pro_Personel_Listesi'
    df_temiz.to_sql(TABLO_ADI, con=engine, if_exists='replace', index=False)
    
    print(f"\n BAŞARILI! Veriler '{TABLO_ADI}' tablosuna güvenle aktarıldı.")

# --- HATA YAKALAMA BLOĞU (EXCEPT) ---
except FileNotFoundError:
    print(f"\n HATA: '{DOSYA_ADI}' dosyası bulunamadı! Lütfen dosya adını kontrol et.")
    
except sqlalchemy.exc.OperationalError:
    print(f"\n HATA: Veritabanına bağlanılamadı! Server ismini ({SERVER_ADI}) kontrol et.")

except Exception as e:
    print(f"\n BEKLENMEDİK BİR HATA OLUŞTU: {e}")

finally:
    print("\n İşlem Sona Erdi.")
