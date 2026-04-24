# btk-food-scanner
🍽️ FoodScanner: Akıllı Alerji Asistanı
Gıda ürünlerinin içindekiler listesini fotoğrafla tarayarak alerjen kontrolü yapan yapay zeka destekli bir uygulama.

🚀 Nasıl Çalışır?
OCR (EasyOCR) — Ürün fotoğrafından içindekiler metnini çıkarır
LLM (Mistral) — Metni analiz ederek alerjen riskini değerlendirir
Gradio Arayüzü — Kullanıcı dostu web arayüzü sunar

📦 Kurulum
# Klasöre git
cd FoodScanner

# Kütüphaneleri kur
pip install -r requirements.txt
⚙️ Ayarlar
Hugging Face adresinden ücretsiz bir API token'ı al
main.py içindeki HUGGING_FACE_TOKEN_BURAYA kısmını kendi token'ınla değiştir

▶️ Çalıştırma
python main.py
Uygulama açıldıktan sonra tarayıcında http://127.0.0.1:7860 adresine git.

🎯 Kullanım
Bir gıda ürününün içindekiler listesinin fotoğrafını yükle
Alerjenini yaz (Örn: Süt, Gluten, Fıstık)
Sonucu gör: GÜVENLİ ✅ veya RİSKLİ ⚠️
