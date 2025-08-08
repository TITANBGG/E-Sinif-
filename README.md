
# E-Sınıf – Yapay Zekâ Destekli Eğitim Yönetim Sistemi

E-Sınıf, eğitim kurumları için geliştirilmiş modern ve hafif bir **Eğitim Yönetim Sistemi (LMS)**’dir.  
Öğretmen–öğrenci etkileşimini tek platformda toplar, ders, ödev, sınav ve değerlendirme süreçlerini kolaylaştırır.  
Yapay zekâ desteği ile ödev değerlendirmelerini otomatikleştirir ve kişiselleştirilmiş geri bildirim sunar.

---

🚀 Özellikler

- **Rol tabanlı erişim:** Öğretmen, öğrenci ve yönetici panelleri
- **Ders / Ödev / Sınav yönetimi:** Oluşturma, düzenleme, silme
- **Yapay zekâ ile otomatik değerlendirme:**  
  - **Google Gemini API** kullanarak ödevleri analiz eder  
  - Açıklamalı puanlama ve geliştirme önerileri verir
- **JWT tabanlı kimlik doğrulama:** Güvenli oturum yönetimi
- **Raporlama modülü:** Performans ve başarı analizleri
- **Modern arayüz:** HTML, CSS, JavaScript + responsive tasarım
- **Hafif ve hızlı:** SQLite veritabanı + FastAPI backend
- **Statik dosya yönetimi:** FastAPI `StaticFiles` ile HTML/CSS/JS servis etme

---

 🛠 Kullanılan Teknolojiler

- **Backend:** Python, FastAPI
- **Frontend:** HTML5, CSS3, JavaScript
- **Veritabanı:** SQLite + SQLAlchemy ORM
- **Kimlik Doğrulama:** JWT (JSON Web Token)
- **Yapay Zekâ API:** Google Gemini AI API
- **Veri Doğrulama:** Pydantic
- **Bağımlılık Yönetimi:** pip + `requirements.txt`

---

## 📂 Proje Yapısı

```

E-Sinif/
│
├── main.py                # FastAPI giriş noktası, API endpoint’leri
├── crud.py                 # CRUD işlemleri
├── models.py               # SQLAlchemy veri modelleri
├── schemas.py              # Pydantic şemaları
├── database.py             # Veritabanı bağlantısı
├── utils.py                # Yardımcı fonksiyonlar (şifre doğrulama vb.)
├── auto\_evaluate.py        # Gemini API ile otomatik değerlendirme
│
├── static/                 # Statik dosyalar
│   ├── style.css
│   ├── uuid.js
│   └── ...
│
├── templates/              # HTML şablonları
│   ├── index.html
│   ├── ogrenci-panel.html
│   ├── ogretmen-panel.html
│   ├── degerlendir.html
│   └── raporlama.html
│
├── requirements.txt        # Python bağımlılıkları
└── README.md               # Proje dokümantasyonu

````

---
 ⚙️ Kurulum

1️⃣ **Depoyu klonla**
```bash
git clone https://github.com/TITANBGG/E-Sinif-.git
cd E-Sinif-
````

2️⃣ **Sanal ortam oluştur ve bağımlılıkları yükle**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

3️⃣ **.env dosyasını oluştur**

```env
APP_ENV=dev
DATABASE_URL=sqlite:///./e_sinif.db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

GEMINI_API_KEY=your_gemini_api_key
```

4️⃣ **Uygulamayı çalıştır**

```bash
uvicorn main:app --reload
```

5️⃣ **Tarayıcıdan eriş**

```
http://127.0.0.1:8000
```

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

---

🤖 Yapay Zekâ Entegrasyonu (Gemini API)

* `auto_evaluate.py` dosyasında, öğrenci ödevleri **Gemini AI**’a gönderilir.
* Model, belirlenen rubriklere göre **puan** ve **açıklama** döner.
* Öğretmen, AI değerlendirmesini onaylayabilir veya düzenleyebilir.

Örnek kullanım:

```python
from auto_evaluate import evaluate_assignment

result = evaluate_assignment(submission_text)
print(result['score'], result['feedback'])
```

---

🔑 Kimlik Doğrulama

* **JWT** kullanır.
* `utils.py` içinde şifre doğrulama fonksiyonu bulunur.
* Tüm korumalı endpoint’ler `Authorization: Bearer <token>` başlığı ister.

---

📊 Raporlama

* **`raporlama.html`** ile öğrenci bazlı, ders bazlı ve ödev bazlı raporlar alınabilir.
* Performans metrikleri, yapay zekâ değerlendirme sonuçları ile birleştirilir.

---

 📌 Yol Haritası

* [ ] Çoklu dil desteği (TR/EN)
* [ ] Docker desteği
* [ ] Gelişmiş bildirim sistemi
* [ ] Mobil uyumlu arayüz geliştirmeleri
* [ ] Öğrenci ilerleme takibi için grafikler

---

🤝 Katkı

Katkıda bulunmak için:

1. Depoyu forklayın
2. Yeni bir dal açın (`git checkout -b feature/ozellik`)
3. Değişiklikleri yapın ve commit edin
4. Pull request gönderin

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

```

---

Ali 
