import os
import json
import tempfile
from fastapi import UploadFile
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai

# .env dosyasını yükle
load_dotenv()

# Gemini API'yi yapılandır
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# PDF dosyasından metin çıkaran yardımcı fonksiyon
def extract_text_from_pdf(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

# Gemini ile değerlendirme yapan ana fonksiyon
def evaluate_homework_with_gemini(text: str) -> dict:
    prompt = f"""
Aşağıdaki ödevi aşağıdaki 5 kritere göre değerlendir:

1. Anlatım Bütünlüğü (coherence)
2. Kaynak Kullanımı (sources)
3. Yorum Gücü (reasoning)
4. Dil ve Anlatım (language)
5. Genel Geri Bildirim (feedback)

Her ölçüt için % puan ver ve son olarak bir toplam puan (total_score) hesapla.

Lütfen cevabı yalnızca şu JSON formatında ver:

{{
  "coherence": int,
  "sources": int,
  "reasoning": int,
  "language": int,
  "feedback": "metinsel yorum",
  "total_score": int
}}

ÖDEV METNİ:
\"\"\"
{text}
\"\"\"
"""

    # Gemini'ye isteği gönder
    response = model.generate_content(prompt)

    # Geri dönen cevabı terminalde göster (debug için)
    print("💬 Gemini'den gelen yanıt:")
    print(response.text)

    # JSON parse etmeyi dene
    try:
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "raw": response.text
        }

@app.post("/auto-evaluate", response_model=schemas.EvaluationOut)
def auto_evaluate(file: UploadFile = File(...), db: Session = Depends(get_db)):
    text = extract_text_from_pdf(file)
    result = evaluate_homework_with_gemini(text)

    # Geçici olarak assignment_id = 1 olarak veriyoruz
    result["assignment_id"] = 1

    evaluation_data = schemas.EvaluationCreate(**result)
    saved = crud.create_ai_evaluation(db, evaluation_data)
    return saved
