# 📄 OCR Financial Report

Aplikasi web modern untuk ekstraksi teks dan data terstruktur dari dokumen PDF dan gambar menggunakan Mistral AI.

## ✨ Fitur Utama

- **📄 Multi-format Support**: PDF, PNG, JPG, JPEG, WebP
- **🤖 Advanced OCR**: Menggunakan Mistral OCR API untuk akurasi tinggi
- **📊 Structured Data Extraction**: Ekstraksi otomatis informasi keuangan
- **💾 Multiple Export Options**: JSON, TXT format
- **📜 Processing History**: Tracking riwayat proses
- **🎨 Modern UI**: Interface yang user-friendly dengan Streamlit
- **⚡ Real-time Progress**: Progress bar dan status updates

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Mistral API Key

### Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd ocr-financial-report
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open browser**
   Aplikasi akan otomatis terbuka di `http://localhost:8501`

## 🔧 Configuration

### API Key Setup

**Method 1: Using .env File (Recommended)**
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` file dan masukkan API key Anda:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```
3. Aplikasi akan otomatis load API key dari environment

**Method 2: Manual Entry**
1. Buka Mistral AI Console (https://console.mistral.ai/)
2. Dapatkan API Key Anda
3. Masukkan API Key di sidebar aplikasi

### Environment Variables
- `MISTRAL_API_KEY`: Your Mistral API key (required)
- `MISTRAL_OCR_MODEL`: OCR model (default: mistral-ocr-latest)
- `MISTRAL_CHAT_MODEL`: Chat model (default: ministral-8b-latest)
- `MAX_FILE_SIZE_MB`: Maximum file size (default: 10)
- `SUPPORTED_LANGUAGES`: Supported languages (default: indonesian,english)

### Settings Options
- **Output Language**: Pilih bahasa output (Indonesian/English)
- **Include Raw OCR**: Sertakan teks OCR mentahan dalam hasil
- **Model Configuration**: View current OCR and Chat models from environment

## 📱 Cara Penggunaan

1. **Upload Dokumen**
   - Klik "Browse files" atau drag & drop
   - Pilih file PDF atau gambar

2. **Proses OCR**
   - Klik tombol "Start OCR Processing"
   - Tunggu proses selesai dengan progress bar

3. **Lihat Hasil**
   - **Tab Structured Data**: Data terstruktur dalam format JSON
   - **Tab Raw OCR Text**: Teks mentahan hasil OCR
   - **Tab Download**: Download hasil dalam berbagai format

4. **Download Results**
   - Structured Data (JSON)
   - Raw Text (TXT)
   - Complete Result (JSON)

## 🏗️ Arsitektur Aplikasi

```
ocr_financial_report/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── .env.example          # Environment variables template
├── .env                  # Environment variables (create this)
├── ocr_pdf.py           # PDF processing (original code)
└── ocr_image.py         # Image processing (original code)
```

## 🔥 Features Detail

### OCR Processing
- **PDF Documents**: Multi-page PDF processing dengan Mistral OCR
- **Image Processing**: Single image OCR dengan high accuracy
- **Language Support**: Indonesian dan English output
- **Error Handling**: Comprehensive error management

### Data Extraction
- **Bank Information**: Nama bank, cabang, alamat
- **Report Information**: Jenis laporan, periode, tanggal
- **Financial Data**: Total aset, liabilitas, ekuitas, dll.
- **Structured Output**: JSON format untuk easy integration

### User Interface
- **Responsive Design**: Works on desktop dan mobile
- **Progress Tracking**: Real-time processing status
- **History Tracking**: Riwayat proses 5 terakhir
- **Tab Navigation**: Organized result viewing

## 📊 Contoh Output

### Structured Data Example
```json
{
    "nama_bank": "Bank Central Asia",
    "jenis_laporan": "Laporan Keuangan Tahunan",
    "periode_laporan": "2024",
    "total_aset": "1.234.567.890",
    "total_liabilitas": "987.654.321"
}
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **OCR Engine**: Mistral AI
- **Environment Management**: python-dotenv
- **Data Format**: JSON
- **File Processing**: PDF, Images

## 🔒 Security & Privacy

- **Environment Variables**: API key disimpan di .env file
- **No File Storage**: Files tidak disimpan secara permanen
- **Temporary Processing**: Files dihapus setelah proses
- **API Key Validation**: Format validation untuk API key
- **Local Processing**: Processing dilakukan di server Anda

## ⚠️ Troubleshooting

### Common Issues

**1. API Key Issues**
- Pastikan API key valid dan ada credits
- Format API key harus dimulai dengan 'h_', 'm_', atau 'c_'
- Cek apakah .env file sudah dibuat dengan benar

**2. Installation Issues**
```bash
# Jika ada error dengan dependencies
pip install --upgrade streamlit mistralai python-dotenv

# Jika environment variables tidak terload
pip install python-dotenv==1.0.0
```

**3. File Upload Issues**
- Max file size: 10MB (dapat diubah di .env)
- Supported formats: PDF, PNG, JPG, JPEG, WebP
- Pastikan file tidak corrupted

**4. Processing Issues**
- Pastikan koneksi internet stabil
- Cek status Mistral API di console
- Restart aplikasi jika ada error yang persisten

## 📝 Notes

- Pastikan koneksi internet stabil
- API Key harus valid dan memiliki credits
- File size limits: Max 10MB per file
- Processing time: 5-30 detik tergantung complexity

## 🤝 Support

Jika ada issues atau pertanyaan:
1. Check API Key validity
2. Verify file format dan size
3. Ensure stable internet connection
4. Check Mistral API status

## 📄 License

MIT License - feel free to use dan modify sesuai kebutuhan.

---

**Built with ❤️ using Streamlit & Mistral AI**