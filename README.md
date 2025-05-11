# ⚖️ TSK İç Hizmet Asistanı
TSK İç Hizmet Kanunu içerisinde hızlıca sorgu yapmak için yardımcı bir asistandır. Kısa ve net bilgiler verir..

## 🛠️ Kullanılan Teknolojiler

-   **FastAPI** – Backend servisleri ve API yönetimi.# 🍳 Mutfak Asistanı


## 🌐 Deploy Link
- [https://mutfak-asistani.streamlit.app/](https://mutfak-asistani.streamlit.app/)

## ✨ Özellikler

- 📝 Metin tabanlı arama
  ⚖️  TSK İç Hizmet Kanunu odaklı
- 📋 Detaylı, kısa, net ve güvenilir biilgiler

## 🚀 Kurulum

### Ön Koşullar

- Python 3.10 veya üzeri

### Adımlar

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. `.env` dosyasını oluşturun ve Gemini API anahtarınızı ekleyin:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   
   > API anahtarını [Google AI Studio](https://aistudio.google.com/app/apikey) adresinden alabilirsiniz.

3. Uygulamayı çalıştırın:
   ```bash
   streamlit run app.py
   ```

## 📖 Kullanım

1. Uygulamayı başlattıktan sonra, web tarayıcınızda otomatik olarak açılacaktır (genellikle http://localhost:8501).
2. **Metin ile sorgu girin**: Öğrenmek istediğiniz kavramları net bir şekilde yazarak girebilirsiniz.
3. Asistan, girdiğiniz net sorgulara göre size kısa, net ve güvenilir cevapları yorum katmadan sunacaktır.




## 📂 Proje Yapısı
"""
tsk-chatbot/
├── .env                            # Google Gemini API anahtarını içerir
├── app.py                         # Streamlit uygulamasının ana Python dosyası
├── vectorstore/                   # FAISS vektör veritabanı dosyaları (index.faiss, index.pkl vs.)
│   ├── index.faiss
│   └── index.pkl
├── tsk_mevzuat_dosyalari/         # Tüm kaynak PDF mevzuatların bulunduğu klasör
│   ├── tskichizmetkanunu.pdf
│   ├── tsk_disiplin_kanunu.pdf
│   ├── tsk_personel_kanunu.pdf
│   └── tsk_ic_hizmet_yonetmeligi.pdf
├── requirements.txt               # Proje bağımlılıklarını listeler
└── README.md                      # Proje açıklaması ve kullanım bilgileri (isteğe bağlı)
"""

## 🗃️ Açıklamalar

- ** app.py: Streamlit ile çalışan ana uygulama dosyası.

- ** .env: GOOGLE_API_KEY="..." satırını içerir. Güvenlik için .gitignore'a eklenmeli.

- ** vectorstore/: FAISS veritabanı burada saklanır. İlk çalıştırmada oluşturulur.

- ** tsk_mevzuat_dosyalari/: Tüm kaynak PDF’leri buraya koyarsın. Uygulama klasördeki tüm .pdf dosyalarını otomatik işler.

- ** requirements.txt

## 🚀 Tech Stack:
- ** Generation Model: Google Gemini API. "gemini 2.0-flash"
- ** Embedding Model: GoogleGenerativeAIEmbeddings(model="models/embedding-001")
- ** Vector Database: FAISS
- ** RAG Pipeline Framework: LangChain
----------
