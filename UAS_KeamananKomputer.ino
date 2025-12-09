// --- DEFINISI PIN ---
const int PIN_SENSOR_A0 = A0;   // Pin Analog MQ-135 A0
const int PIN_KIPAS = 8;        // Pin Digital untuk kontrol Basis Transistor (Kipas)

// --- AMBANG BATAS (THRESHOLD) DENGAN HYSTERESIS ---
// Ambang batas A0 (Analog) untuk Kipas ON
const int THRESHOLD_HIGH_A0 = 350; 
// Ambang batas A0 (Analog) untuk Kipas OFF
const int THRESHOLD_LOW_A0 = 330; 

// Variabel untuk melacak status kipas saat ini
bool kipas_aktif = false; 

// --- FUNGSI MAPPING PPM ---
// Fungsi perkiraan konversi dari nilai Analog (0-1023) menjadi PPM.
int mapToPPM(int nilaiAnalog) {
    // Mapping 0-1023 ke 0-1000 PPM (Contoh)
    return map(nilaiAnalog, 0, 1023, 0, 1000); 
}

void setup() {
    pinMode(PIN_KIPAS, OUTPUT);
    Serial.begin(9600); // BAUD RATE HARUS SAMA DENGAN PYTHON
    
    digitalWrite(PIN_KIPAS, LOW);
    Serial.println("==================================================");
    Serial.println("Sistem Pemantau Kualitas Udara Aktif (MQ-135)");
    Serial.print("Amb. Kipas ON (A0): "); Serial.println(THRESHOLD_HIGH_A0);
    Serial.print("Amb. Kipas OFF (A0): "); Serial.println(THRESHOLD_LOW_A0);
    Serial.println("==================================================");
}

void loop() {
    int nilaiSensorA0 = analogRead(PIN_SENSOR_A0);
    int kualitasUdaraPPM = mapToPPM(nilaiSensorA0);

    // --- TAMPILAN OUTPUT SERIAL ---
    Serial.print("Kualitas Udara Saat Ini: ");
    Serial.print(kualitasUdaraPPM);
    Serial.print(" ppm");

    // --- LOGIKA KONTROL KIPAS DENGAN HYSTERESIS ---
    
    // 1. Logika untuk MENGHIDUPKAN Kipas
    if (nilaiSensorA0 > THRESHOLD_HIGH_A0 && !kipas_aktif) {
        digitalWrite(PIN_KIPAS, HIGH); 
        kipas_aktif = true; 
        Serial.println(" | Kipas ON (Udara Buruk).");
    } 
    
    // 2. Logika untuk MEMATIKAN Kipas
    else if (nilaiSensorA0 <= THRESHOLD_LOW_A0 && kipas_aktif) {
        digitalWrite(PIN_KIPAS, LOW); 
        kipas_aktif = false; 
        Serial.println(" | Kipas OFF (Udara Normal).");
    }
    
    // 3. Status Stabil
    else {
        if (kipas_aktif) {
            Serial.println(" | Kipas ON.");
        } else {
            Serial.println(" | Kipas OFF.");
        }
    }
    
    delay(1000); // Kirim data setiap 1 detik
}