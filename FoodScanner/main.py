import os
import sys

# Windows konsol encoding sorununu çöz
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    _old_stdout = sys.stdout
    _old_stderr = sys.stderr
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)

import gradio as gr
import easyocr
import cv2
import numpy as np
from huggingface_hub import InferenceClient

# OCR modelini başlat (Türkçe + İngilizce)
try:
    reader = easyocr.Reader(['tr', 'en'])
except Exception as e:
    print(f"⚠️ OCR modeli yüklenirken hata: {e}")
    reader = None

# Hugging Face LLM - API anahtarını ortam değişkeninden al
api_key = os.environ.get("HF_API_KEY", "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")
client = InferenceClient(api_key=api_key)


def preprocess_image(image):
    """Görüntüyü OCR için optimize et"""
    # 1. Görüntüyü büyüt (2x) - küçük yazılar için çok önemli
    h, w = image.shape[:2]
    image = cv2.resize(image, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
    
    # 2. Gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # 3. Kontrast artırma (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    
    # 4. Gürültü azaltma
    gray = cv2.fastNlMeansDenoising(gray, h=10)
    
    # 5. Adaptive threshold - metin ve arka planı ayır
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    
    # 6. Morfolojik işlem - harfleri netleştir
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return gray, binary


def scanner(image, alerjen):
    if image is None:
        return "⚠️ Lütfen bir fotoğraf yükleyin."
    if not alerjen or alerjen.strip() == "":
        return "⚠️ Lütfen alerjen bilgisi girin."
    if reader is None:
        return "❌ OCR modeli yüklenemedi. Lütfen uygulamayı yeniden başlatın."
    
    # 1. Görüntü ön işleme
    gray, binary = preprocess_image(image)
    
    # 2. Birden fazla yöntemle OCR dene, en iyi sonucu al
    results = []
    
    # Orijinal renkli görüntüden oku
    r1 = reader.readtext(image, detail=0, paragraph=True)
    results.append(" ".join(r1))
    
    # Gri tonlama görüntüden oku
    r2 = reader.readtext(gray, detail=0, paragraph=True)
    results.append(" ".join(r2))
    
    # Binary (siyah-beyaz) görüntüden oku
    r3 = reader.readtext(binary, detail=0, paragraph=True)
    results.append(" ".join(r3))
    
    # En uzun sonucu seç (genelde en detaylı olan)
    full_text = max(results, key=len)
    
    if not full_text.strip():
        return "❌ Fotoğraftan metin okunamadı.\n\n💡 İpuçları:\n- Kamerayı içindekiler listesine yaklaştırın\n- Yazının net ve aydınlık olduğundan emin olun\n- Ürünü düz tutun"
    
    # 3. LLM'e sor
    prompt = (
        f"Sen bir gıda güvenliği uzmanısın. Aşağıda bir gıda ürününün içindekiler listesi var.\n"
        f"Bu metin OCR ile okunduğu için bazı hatalar olabilir, lütfen en mantıklı yorumu yap.\n\n"
        f"İçindekiler listesi: {full_text}\n\n"
        f"Kullanıcının alerjisi: {alerjen}\n\n"
        f"Lütfen şunları yap:\n"
        f"1. Önce okunan metindeki içindekiler listesini düzeltip listele\n"
        f"2. Sonra '{alerjen}' alerjeni açısından 'GÜVENLİ ✅' veya 'RİSKLİ ⚠️' olarak değerlendir\n"
        f"3. Kısa bir açıklama yaz\n"
        f"Türkçe cevap ver."
    )
    
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        llm_result = response.choices[0].message.content
        return f"🤖 Analiz Sonucu:\n\n{llm_result}"
    except Exception as e:
        return f"❌ Hata: {str(e)}"


# Gradio Arayüzü - Webcam ile
with gr.Blocks(title="FoodScanner: Akıllı Alerji Asistanı") as demo:
    gr.Markdown(
        """
        # 🍽️ FoodScanner: Akıllı Alerji Asistanı
        **Webcam ile ürünün içindekiler listesini göster** → Alerjen riski öğren!
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            webcam = gr.Image(
                sources=["upload"],
                type="numpy",
                label="📷 İçindekiler Listesi Fotoğrafı Yükle",
            )
            alerjen_input = gr.Textbox(
                label="⚠️ Alerjenin nedir?",
                placeholder="Örn: Süt, Gluten, Fıstık, Yumurta...",
                lines=1,
            )
            scan_btn = gr.Button("🔍 Tara ve Analiz Et", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            output = gr.Textbox(
                label="📊 Sonuç",
                lines=15,
            )
    
    scan_btn.click(fn=scanner, inputs=[webcam, alerjen_input], outputs=output)
    
    gr.Markdown(
        """
        ---
        💡 **İpuçları:**
        - 📏 Kamerayı **içindekiler listesine yakın** tutun
        - 💡 **İyi aydınlatma** altında çekin
        - 📐 Ürünü **düz** tutun, eğmeyin
        - 🔍 Yazıların **net görünmesi** önemli
        """
    )

demo.launch(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="amber"))
