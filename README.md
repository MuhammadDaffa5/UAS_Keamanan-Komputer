# Sistem Otomatis Pemantau & Kontrol Kualitas Udara (AQMS)

**Oleh: M. Daffa' al haq.S (09030282327028), Muhammad Rifki (09030582327082), Siti Anisah Chyntia Bella (09030282327019)**

## Deskripsi Proyek

Proyek ini mengimplementasikan sistem **Sistem Otomatis Pemantau dan Kontrol Kualitas Udara (AQMS)** menggunakan Arduino Uno dan sensor MQ-135. Sistem ini dirancang untuk mendeteksi polutan gas dan secara otomatis mengaktifkan kipas (ventilasi) sebagai tindakan korektif ketika kualitas udara memburuk.

**Fitur Tambahan:** Proyek ini juga mencakup simulasi **Serangan Man-in-the-Middle (MITM) Serial** menggunakan Python di Kali Linux untuk mendemonstrasikan kerentanan komunikasi titik-ke-titik.

---

## Komponen Hardware yang Digunakan

KOMPONEN HARDWARE SISTEM AQMS

1. Mikrokontroler:
   - Nama: Arduino Uno
   - Fungsi Utama: Otak pemroses data dan pengontrol aktuator.

2. Sensor Gas:
   - Nama: MQ135
   - Fungsi Utama: Input, mengukur konsentrasi polutan gas dan menghasilkan nilai Analog (A0).

3. Aktuator:
   - Nama: Kipas DC / Ventilasi
   - Fungsi Utama: Output, aksi korektif untuk memperbaiki kualitas udara.
---

## Cara Kerja Sistem AQMS (Fokus pada Stabilitas)

Sistem bekerja dalam siklus tertutup dengan prinsip Hysteresis untuk menjamin stabilitas dan umur panjang komponen.

1.  **Pengukuran:** Sensor MQ-135 membaca tegangan polusi (Pin A0), yang kemudian dikonversi menjadi perkiraan nilai **PPM** (*Parts Per Million*).
2.  **Keputusan Hysteresis:** Nilai PPM dievaluasi menggunakan dua ambang batas: Threshold HIGH (Kipas ON) dan Threshold LOW (Kipas OFF).
    * **Tujuan:** Logika ini mencegah kipas sering ON/OFF (*flickering*) ketika nilai sensor berfluktuasi di dekat ambang batas tunggal.
3.  **Aksi Korektif:** Jika nilai PPM melewati Threshold HIGH, Arduino menyetel Pin D8 ke HIGH, mengaktifkan kipas. Kipas akan tetap ON sampai PPM turun di bawah Threshold LOW.

---

## Demonstrasi Serangan Man-in-the-Middle (MITM) Serial

### Mekanisme Serangan

Serangan MITM ini terjadi di jalur komunikasi USB/Serial. Skrip Python di Kali Linux berfungsi sebagai perantara yang mencegat data sebelum mencapai *Serial Monitor*.

1.  **Intercept & Cekal:** Skrip Python di Kali Linux mengambil kendali eksklusif atas port serial Arduino.
2.  **Analisis:** Skrip membaca data *real-time* dari Arduino (PPM asli) dan menggunakan Regex untuk mengekstrak nilainya.
3.  **Modifikasi Dinamis:** Skrip menerapkan logika kontra-serangan, yaitu mengubah nilai PPM asli menjadi nilai palsu yang bersifat acak dan berlawanan (misalnya, jika PPM asli menunjukkan Udara Buruk, skrip melaporkan Udara Aman 50-150 ppm).
4.  **Output Palsu:** Data yang sudah dimanipulasi ditampilkan ke terminal Kali Linux, menipu pengguna yang memantau sistem.

### Persyaratan & Eksekusi Serangan

* **Platform:** Kali Linux Virtual Machine (VM) dengan USB Passthrough aktif.
* **Dependencies:** Python 3 dan Library pyserial.
    ```
    pip install pyserial
    ```
* **Langkah Eksekusi:**

    1.  Tentukan port serial Arduino di Kali (`/dev/ttyACM0` atau `/dev/ttyUSB0`).
    2.  Pastikan SERIAL_PORT di mitm_serial.py sudah dikonfigurasi.
    3.  Jalankan skrip (setelah mengaktifkan venv jika digunakan):
        ```
        python3 mitm_serial.py
