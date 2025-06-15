# 🕌 Prediksi Biaya Haji Indonesia - RAG Agentic AI

![Versi Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Streamlit-1.35.0-red?style=for-the-badge&logo=streamlit)
![Lisensi](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
[![GitHub Stars](https://img.shields.io/github/stars/NAMA_USER_ANDA/NAMA_REPO_ANDA?style=for-the-badge&logo=github)](https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA/stargazers)

Analisis dan prediksi biaya penyelenggaraan ibadah haji (BPIH) di Indonesia menggunakan model _Ensemble Machine Learning_ dan diperkaya dengan sistem _Retrieval-Augmented Generation (RAG)_ untuk analisis berbasis data riil.

---

### ✨ Demo Aplikasi

Pernahkah Anda bertanya-tanya berapa perkiraan biaya haji di masa depan? Aplikasi ini memberikan visualisasi data historis dan prediksi yang didukung oleh AI untuk menjawab pertanyaan tersebut.

*(Tips Keren: Rekam layar aplikasi Anda dan ubah menjadi GIF, lalu letakkan di sini. Ini akan membuat README Anda 10x lebih menarik! Gunakan alat seperti [LICEcap](https://www.cockos.com/licecap/) atau [ScreenToGif](https://www.screentogif.com/))*

![Demo Aplikasi](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbTdyZ2s4b29tZ2w0OHZsc2NkN2xwZHg5N2hpd2ZhaTFxYm9nMXNndCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyE/giphy.gif)
*(Ganti gambar di atas dengan screenshot atau GIF demo aplikasi Anda)*

---

### 🚀 Fitur Utama

-   **📈 Visualisasi Data Historis**: Grafik interaktif biaya haji rata-rata nasional dari tahun 2016 hingga 2025 berdasarkan data Keppres RI.
-   **🔮 Prediksi Biaya Masa Depan**: Prediksi biaya haji untuk 5 tahun ke depan menggunakan model _Polynomial Regression_ yang di-ensemble dengan metode CAGR untuk hasil yang lebih robust.
-   **🤖 Analisis AI dengan RAG**: Ajukan pertanyaan dalam bahasa natural (contoh: "Kenapa biaya haji 2023 naik drastis?") dan dapatkan jawaban yang dihasilkan AI berdasarkan konteks data riil yang dimiliki.
-   **🗺️ Perbandingan Regional**: Analisis perbandingan biaya haji antar embarkasi utama di Indonesia (Jakarta, Surabaya, Medan, Makassar, Aceh).
-   **📊 Dasbor Interaktif**: Tampilan metrik utama seperti CAGR, perubahan tahunan, dan biaya per embarkasi dalam satu dasbor yang responsif.

---

### 🛠️ Teknologi yang Digunakan

-   **Backend & Frontend**:
    -   ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
    -   ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
-   **Analisis Data & ML**:
    -   ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
    -   ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
    -   ![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
-   **Visualisasi Data**:
    -   ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

---

### ⚙️ Instalasi & Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer lokal Anda.

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git](https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git)
    cd NAMA_REPO_ANDA
    ```

2.  **Buat dan aktifkan virtual environment (sangat disarankan):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Opsional) Konfigurasi API Keys:**
    Jika Anda ingin menggunakan fitur AI yang lebih canggih, buat file `.env` dan masukkan API key Anda (fitur ini untuk pengembangan modular di masa depan).
    ```
    OPENROUTER_API_KEY="sk-or-..."
    ```

5.  **Jalankan aplikasi Streamlit:**
    ```bash
    streamlit run app.py
    ```
    Buka browser Anda dan akses `http://localhost:8501`.

---

### 📄 Sumber Data

Aplikasi ini menggunakan data Biaya Penyelenggaraan Ibadah Haji (BPIH) yang bersumber langsung dari **Keputusan Presiden (Keppres) Republik Indonesia** dari tahun 2016 hingga 2025. Hal ini memastikan bahwa analisis dan prediksi didasarkan pada data yang valid dan akurat.

---

### 💡 Rencana Pengembangan

Proyek ini masih terus berkembang. Beberapa rencana ke depan:
-   [ ] Menambahkan data dari lebih banyak embarkasi di seluruh Indonesia.
-   [ ] Integrasi dengan API kurs mata uang real-time (IDR/SAR & IDR/USD).
-   [ ] Mengembangkan model prediksi yang lebih canggih (misalnya ARIMA atau Prophet).
-   [ ] Fitur kalkulator tabungan haji personal.

---

### 📜 Lisensi

Proyek ini didistribusikan di bawah **Lisensi MIT**. Lihat file `LICENSE` untuk informasi lebih lanjut.

---

### 👨‍💻 Developer

Dibuat dengan ❤️ oleh **MS Hadianto [sopian.hadianto@gmail.com]**.

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/mshadianto)
