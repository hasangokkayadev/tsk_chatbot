# ⚖️ TSK İç Hizmet Asistanı
TSK İç Hizmet Kanunu içerisinde hızlıca sorgu yapmak için yardımcı bir asistandır.
Mevzuat'ın kapsamı geniş olduğu için personelin, istediği bilgiye hızla erişmesi, bilgi karmaşası içerisine düşmesini engelleyerek kısa ve net bilgiler vermesk için tasarlanmıştır.
Chatbot'a verilen kaynak mevzuat çeşitliliği artırılıp bu çalışma ilerletilerek daha farklı içeriklere içtihatlarla birlikte yorum getirilmesi de denenecektir.

----------
## 🛠️ Kullanılan Teknolojiler:

- ** Generation Model: Google Gemini API. "gemini 2.0-flash"
- ** Embedding Model: GoogleGenerativeAIEmbeddings(model="models/embedding-001")
- ** Vector Database: FAISS
- ** RAG Pipeline Framework: LangChain

----------
## 🌐 Deploy Link
- [https://tsk-chatbot.streamlit.app/](https://tsk-chatbot.streamlit.app/)

----------
## Ekran Görüntüsü
- ![image](https://github.com/user-attachments/assets/e8692559-c01e-4185-ac47-ffd75cdcf176)

----------
## Veri Seti  Toplanış/Hazırlanış Metodolojisi
- 📝 Veriseti olarak TSK İç Hizmet Kanunu'nun pdf dokümanu eklenmiştir.
- 📝 def load_pdf_lines(path): şeklinde tanımlanan fonksiyon ile chunklama işlemi satır satır parçalama şeklinde yapılmıştır.
- 📝 FAISS vektör db ile bu parçalar indexlenmiş, işlem ve depolama yükü hafifletilmiştir.
- 📝 LLM modeli olarak gemini-flash-2.0 ile embedding model olarak da embeddings-001 modelleri bir arada kullanılarak, deneyimlenen farklı modellerin zayıflıklarından sonra bu uygulama özelinde mükemmel bir uyum yakalanmıştır.

---------- 
## ✨ Özellikler ve Kullanım Senaryosu

- ⚖️ TSK İç Hizmet Kanunu özelinde Metin tabanlı arama.
- ⚖️ **RAG (Retrieval-Augmented Generation)** mimarisi ile dinamik içerik sorgulama.
- ⚖️ Detaylı, kısa, net ve güvenilir bilgiler.
- ⚖️ Yanıtla butonu ile sorgulama.
- ⚖️ Temizle butonu ile sorgu geçmişi ve cevapların silinmesi.
- ⚖️ Önbellekleme ile kaynak dokümanın tekrar yüklenmesine gerek olmaması ve hızlı çalışma süresi.

----------
## 🚀 Kurulum

### Ön Koşullar

- Python 3.12 veya üzeri

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
----------
## 📖 Kullanım

1. Uygulamayı başlattıktan sonra, web tarayıcınızda otomatik olarak açılacaktır (genellikle http://localhost:8501).
2. **Metin ile sorgu girin**: Kavramlar bir çok yerde tekrar ettiği için, istenilen bağlamda cevaplar elde etmek için, öğrenmek istediğiniz kavramları net bir şekilde yazarak girebilirsiniz.
3. Asistan, girdiğiniz net sorgulara göre size kısa, net ve güvenilir cevapları yorum katmadan sunacaktır.
4. Eğer kullanıcı açıkça yorum isterse (“yorumla”, “fikir yürüt”, “sence” vs. gibi ifadelerle) o zaman yasal bir uyarı ile yorumda bulunacaktır.

----------
## 📂 Proje Yapısı
```tsk-chatbot/
├── .env                           # Google Gemini API anahtarını içerir
├── app.py                         # Streamlit uygulamasının ana Python dosyası
├── vectorstore/                   # FAISS vektör veritabanı dosyaları (index.faiss, index.pkl vs.)
│   ├── index.faiss
│   └── index.pkl
├── tsk_mevzuat_dosyalari/         # Tüm kaynak PDF mevzuatların bulunduğu klasör
│   ├── tskichizmetkanunu.pdf
├── requirements.txt               # Proje bağımlılıklarını listeler
└── README.md                      # Proje açıklaması ve kullanım bilgileri (isteğe bağlı)
```

----------
## 🗃️ Açıklamalar

- ** app.py: Streamlit ile çalışan ana uygulama dosyası.

- ** .env: GOOGLE_API_KEY="..." satırını içerir. Güvenlik için .gitignore'a eklenmeli.

- ** vectorstore/: FAISS veritabanı burada saklanır. İlk çalıştırmada oluşturulur.

- ** tsk_mevzuat_dosyalari/: Tüm kaynak PDF’leri buraya koyarsın. Uygulama klasördeki tüm .pdf dosyalarını otomatik işler.

- ** requirements.txt

----------
## 📞 İletişim ve Destek

Proje ile ilgili öneri ve sorularınız için:

-   **Hasan GÖKKAYA** - hasangokkayadev@gmail.com
-   www.linkedin.com/in/hasangokkayadev
