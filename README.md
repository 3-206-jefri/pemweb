# Pertemuan 13: Product Review Analyzer

### Deskripsi Singkat

**Product Review Analyzer** adalah aplikasi web full-stack yang dirancang untuk menganalisis ulasan produk menggunakan teknologi AI terkini. Aplikasi ini menggabungkan **sentiment analysis** (analisis sentimen) dan **key points extraction** (ekstraksi poin penting) untuk memberikan wawasan mendalam tentang setiap ulasan produk.

Aplikasi menyimpan semua hasil analisis ke **database** sehingga data dapat diakses kapan saja dan ditampilkan dalam bentuk riwayat ulasan yang terstruktur.

Dibuat menggunakan:
- **Backend**: Python + Pyramid Web Framework + SQLAlchemy
- **Frontend**: React 19 + Vite + Axios
- **Database**: PostgreSQL (production) / SQLite (development)
- **AI/API**: Hugging Face (sentiment) + Google Gemini (key points)

---

## Fitur Utama

| No | Fitur | Status | Deskripsi |
|:--:|:------|:------:|:----------|
| 1 | **Input Ulasan** | ✅ | Pengguna dapat menginput ulasan produk dalam bentuk teks. |
| 2 | **Analisis Sentimen** | ✅ | Menganalisis sentimen ulasan (positif/negatif/netral) menggunakan Hugging Face. |
| 3 | **Ekstraksi Poin Penting** | ✅ | Mengekstraksi poin-poin penting dari ulasan menggunakan Google Gemini AI. |
| 4 | **Tampilan Hasil** | ✅ | Menampilkan hasil analisis (sentimen + poin penting) secara langsung. |
| 5 | **Riwayat Ulasan** | ✅ | Menampilkan semua ulasan yang telah dianalisis dalam format tabel. |
| 6 | **Integrasi Database** | ✅ | Menyimpan semua hasil analisis ke database (PostgreSQL/SQLite). |
| 7 | **Loading State** | ✅ | Menampilkan indikator loading saat sedang menganalisis. |
| 8 | **Error Handling** | ✅ | Fallback otomatis jika API eksternal tidak tersedia. |

---

## Struktur Proyek

```
Pertemuan 13/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Konfigurasi Pyramid & routes
│   │   ├── views.py                 # Endpoint API
│   │   ├── models.py                # Model SQLAlchemy
│   │   ├── huggingface_helper.py    # Sentiment analysis
│   │   └── genai_helper.py          # Key points extraction
│   ├── development.ini              # Konfigurasi development
│   ├── setup.py                     # Dependencies
│   ├── init_db.py                   # Inisialisasi database
│   └── development.db               # Database SQLite (dev)
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx              # Komponen utama React
│       │   ├── main.jsx             # Entry point
│       │   ├── App.css              # Styling
│       │   └── index.css            # Global styles
│       ├── vite.config.js           # Konfigurasi Vite
│       ├── package.json             # Dependencies
│       ├── dist/                    # Build output
│       └── index.html               # HTML template
└── README.md                        # Dokumentasi ini
```

## Cara Menjalankan

### Setup Backend

1. **Navigasi ke folder backend:**
```powershell
cd backend
```

2. **Buat dan aktifkan virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install pyramid waitress SQLAlchemy python-dotenv requests google-generativeai
```

4. **Jalankan server backend:**
```powershell
pserve .\development.ini
```
Server akan berjalan di: **http://127.0.0.1:6543**

### Setup Frontend

1. **Navigasi ke folder frontend:**
```powershell
cd frontend/frontend
```

2. **Install dependencies:**
```powershell
npm install
```

3. **Build frontend:**
```powershell
npm run build
```

4. **Frontend akan tersedia di:** **http://127.0.0.1:6543** (dilayani oleh backend)

---

## Endpoint API

### 1. POST `/api/analyze-review`

**Fungsi**: Menganalisis ulasan produk baru

**Request:**
```json
{
  "text": "Produk sangat bagus, kualitas terbaik dan harga terjangkau"
}
```

**Response:**
```json
{
  "result": {
    "id": 1,
    "text": "Produk sangat bagus, kualitas terbaik dan harga terjangkau",
    "sentiment": "positive",
    "key_points": ["Kualitas terbaik", "Harga terjangkau"],
    "created_at": "2025-12-12T13:21:44.133307"
  }
}
```

### 2. GET `/api/reviews`

**Fungsi**: Mengambil semua ulasan yang telah dianalisis

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "text": "Produk sangat bagus...",
      "sentiment": "positive",
      "key_points": ["Kualitas terbaik", "Harga terjangkau"],
      "created_at": "2025-12-12T13:21:44.133307"
    }
  ]
}
```

---

## Penjelasan Teknis

### Sentimen Analysis dengan Hugging Face

**Hugging Face** menyediakan model pre-trained untuk mengklasifikasikan sentimen teks:
- Model yang digunakan: `cardiffnlp/twitter-roberta-base-sentiment`
- Output: `positive`, `negative`, atau `neutral`

**Fallback**: Jika API tidak tersedia, sistem akan menggunakan analisis keyword sederhana untuk mendeteksi sentimen secara manual.

**Cara menggunakan:**
1. Dapatkan token dari: https://huggingface.co/settings/tokens
2. Set di environment variable: `HUGGINGFACE_TOKEN`

### Key Points Extraction dengan Google Gemini

**Google Gemini** menggunakan AI generatif untuk mengekstraksi poin-poin penting dari ulasan:
- Model: `gemini-1.5-flash` (cepat dan efisien)
- Output: Array JSON berisi poin-poin utama

**Fallback**: Jika API tidak tersedia, sistem akan mengembalikan array kosong.

**Cara menggunakan:**
1. Dapatkan API key dari: https://aistudio.google.com/app/apikey
2. Set di environment variable: `GEMINI_API_KEY`

### Integrasi Database

Aplikasi menggunakan **SQLAlchemy** sebagai ORM (Object-Relational Mapping) untuk berinteraksi dengan database.

**Development**: Menggunakan **SQLite** (file `development.db`)
**Production**: Menggunakan **PostgreSQL**

**Tabel `reviews`:**

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| id | Integer | Primary key |
| text | Text | Teks ulasan produk |
| sentiment | String | positive/negative/neutral |
| key_points | Text | JSON array poin penting |
| created_at | DateTime | Timestamp pembuatan |

---

## Error Handling

Aplikasi ini dilengkapi dengan mekanisme error handling yang robust:

- ✅ Validasi input JSON
- ✅ Fallback otomatis untuk API yang tidak tersedia
- ✅ Pesan error yang user-friendly
- ✅ Loading state selama proses analisis
- ✅ Database fallback (SQLite jika PostgreSQL tidak tersedia)

## Troubleshooting

### Backend tidak mau start

**Error**: `psycopg2.OperationalError: connection to server failed`

**Solusi**: Backend otomatis akan fallback ke SQLite. Untuk production, pastikan DATABASE_URL sudah benar.

### Frontend tidak muncul (404)

**Error**: `404 Not Found: /index.html`

**Solusi**: Jalankan `npm run build` di folder `frontend/frontend`, lalu restart backend.

### API calls gagal (saat development)

**Solusi**: Pastikan backend berjalan di `http://127.0.0.1:6543` dan axios mengirim request ke endpoint yang benar.

### Sentiment selalu "neutral"

**Penyebab**: API Hugging Face tidak tersedia atau token tidak valid

**Solusi**: 
- Periksa `HUGGINGFACE_TOKEN` di environment
- Verifikasi token di https://huggingface.co/account/tokens

### Key points extraction kosong

**Penyebab**: API Gemini tidak tersedia atau key tidak valid

**Solusi**:
- Periksa `GEMINI_API_KEY` di environment
- Verifikasi key di https://aistudio.google.com/app/apikey

---

## Teknologi yang Digunakan

**Backend:**
- Python 3.13+
- Pyramid (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL / SQLite (Database)
- Hugging Face API (Sentiment Analysis)
- Google Gemini API (Key Points Extraction)

**Frontend:**
- React 19
- Vite (Build Tool)
- Axios (HTTP Client)

---

## Checklist Fitur

✅ Input ulasan produk  
✅ Analisis sentimen dengan Hugging Face  
✅ Ekstraksi poin penting dengan Google Gemini  
✅ Tampilan hasil yang interaktif  
✅ Riwayat semua ulasan  
✅ Integrasi database (PostgreSQL/SQLite)  
✅ Error handling & fallback mechanism  
✅ Loading state indicator  
✅ Dokumentasi lengkap  

---

## Referensi

- Pyramid Documentation: https://docs.pylonsproject.org/projects/pyramid/
- SQLAlchemy: https://docs.sqlalchemy.org/
- React: https://react.dev/
- Vite: https://vite.dev/
- Hugging Face Inference API: https://huggingface.co/docs/inference-api
- Google Gemini API: https://ai.google.dev/

---

**Dibuat oleh:** Jefri Wahyu Fernando Sembiring (NIM: 123140206)  
**Repository:** https://github.com/3-206-jefri/pemweb  
**Terakhir diperbarui:** December 12, 2025
