# 🍽️ FoodScanner: Akıllı Alerji Asistanı

Gıda ürünlerinin içindekiler listesini fotoğrafla tarayarak alerjen kontrolü yapan yapay zeka destekli bir uygulama.

## 🚀 Nasıl Çalışır?

1. **OCR (EasyOCR)** — Ürün fotoğrafından içindekiler metnini çıkarır
2. **LLM (Mistral)** — Metni analiz ederek alerjen riskini değerlendirir
3. **Gradio Arayüzü** — Kullanıcı dostu web arayüzü sunar

## 📦 Kurulum

```bash
# Klasöre git
cd FoodScanner

# Kütüphaneleri kur
pip install -r requirements.txt
```

## ⚙️ Ayarlar

1. [Hugging Face](https://huggingface.co/settings/tokens) adresinden ücretsiz bir API token'ı al
2. `main.py` içindeki `HUGGING_FACE_TOKEN_BURAYA` kısmını kendi token'ınla değiştir

## ▶️ Çalıştırma

```bash
python main.py
```

Uygulama açıldıktan sonra tarayıcında `http://127.0.0.1:7860` adresine git.

## 🎯 Kullanım

1. Bir gıda ürününün **içindekiler listesinin fotoğrafını** yükle
2. **Alerjenini** yaz (Örn: Süt, Gluten, Fıstık)
3. Sonucu gör: **GÜVENLİ ✅** veya **RİSKLİ ⚠️**

