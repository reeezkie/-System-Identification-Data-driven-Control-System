# ⚙️ System Identification & Data-driven Control: Identifikasi Motor DC JGA25
> Pemodelan Matematis Sistem Menggunakan Model ARX Orde Pertama dan Metode Least Squares Estimation (LSE)

[![Status Project](https://img.shields.io/badge/Status-Completed-success.svg)]()
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)]()
[![Arduino](https://img.shields.io/badge/Microcontroller-Arduino%20Uno-orange.svg)]()
[![Institution](https://img.shields.io/badge/Universitas-Brawijaya-red.svg)]()

Repositori ini berisi kode sumber (*embedded code* & *analysis script*), data eksperimen, dan laporan lengkap untuk praktikum **System Identification & Data-driven Control System**. Proyek ini bertujuan untuk melakukan identifikasi sistem pada **Motor DC JGA25** guna mendapatkan model matematis orde pertama (ARX) berdasarkan data masukan sinyal *Pseudo-Random Binary Sequence* (PRBS) dan keluaran kecepatan motor (*measured velocity*).

---

## 🏛️ Informasi Akademik
* **Mata Kuliah:** Data-driven Control System / Identifikasi Sistem
* **Dosen Pengampu:** Wijaya Kurniawan, S.T., M.T., Ph.D.
* **Institusi:** Fakultas Ilmu Komputer, Universitas Brawijaya (FILKOM UB)

### 👥 Tim Penyusun (Kelompok)
1. **Ayu Halimatus Sa'diyah** (245150300111012)
2. **Rezky Auliasarie** (245150300111014)
3. **Zeyra Rahma Alivia** (245150301111016)

---

## 💡 Latar Belakang & Tujuan
Motor DC merupakan aktuator krusial dalam sistem kendali otomatis. Agar perancangan sistem kendali (*controller*) berjalan optimal, karakteristik dinamika motor harus diketahui melalui proses **Identifikasi Sistem**. 

Proyek ini dirancang untuk:
1. Membangkitkan sinyal uji **PRBS (Pseudo-Random Binary Sequence)** melalui Arduino Uno untuk memberikan variasi masukan duty cycle (30% dan 80%) yang lebih beragam dibandingkan *single-step input*.
2. Membaca pulsa encoder motor DC JGA25 secara *real-time* menggunakan mekanisme *interrupt* dengan waktu sampling ($T_s$) sebesar 50 ms.
3. Membentuk model matematis **Auto-Regressive with Exogenous input (ARX) orde pertama**:
   $$y[k] = a_1 \cdot y[k-1] + b_1 \cdot u[k-1]$$
4. Mengestimasi parameter model ($a_1$ dan $b_1$) menggunakan metode **Least Squares Estimation (LSE)**.
5. Mengevaluasi performa model menggunakan metrik *Mean Squared Error* (MSE), *Root Mean Squared Error* (RMSE), dan koefisien determinasi ($R^2$).

---

## 🛠️ Perangkat Keras & Lunak (Hardware & Software)
### 1. Hardware
* **Arduino Uno:** Pengendali utama, pembangkit sinyal PRBS, PWM, serta pembaca *interrupt* encoder.
* **L298N Motor Driver:** Modul pengendali daya dan arah putaran motor DC.
* **JGA25 DC Motor:** Objek identifikasi sistem yang dilengkapi *Hall-Effect Encoder*.
* **Hall-Effect Encoder:** Sensor pengukur pulsa putaran motor (resolusi 374 *counts per revolution*).
* **Catu Daya Eksternal:** Sumber suplai daya motor DC melalui L298N.
* **Komputer:** Perangkat pengolah data dan analisis Python via komunikasi serial.

### 2. Software
* **Arduino IDE:** Pemrograman mikrokontroler (*firmware*) pengendali PWM dan pembacaan encoder.
* **Python & Libraries (NumPy, Pandas):** Pengolahan data CSV, penyusunan matriks regresi, komputasi Least Squares, serta visualisasi kurva evaluasi.

---

## 📌 Konfigurasi Sistem Pin
| Komponen / Periferal | Pin Arduino Uno |
| :--- | :--- |
| **PWM Pin (ENA)** | Pin 5 |
| **L298N IN1** | Pin 7 |
| **L298N IN2** | Pin 8 |
| **Encoder Channel A** | Pin 2 (Interrupt) |

---

## 📂 Struktur Repositori
```text
├── SYSTEM IDENTIFICATION FUNDAMENTALS.pdf    # Laporan lengkap praktikum (teori, metodologi, & analisis)
├── analysis_system_identification.py        # Skrip Python untuk LSE, prediksi, dan evaluasi model
├── source_code_datadriven.ino               # Kode sumber Arduino (PRBS generation & encoder reading)
└── README.md                                # Dokumentasi proyek
