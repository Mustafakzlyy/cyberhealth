# 🛡️ CyberHealth Desktop

🌐 **Diller:** [Kurdî](README.ku.md) | [Türkçe](README.tr.md) | [English](README.en.md)

> **Son Kullanıcı Dijital Güvenlik ve Sağlık Asistanı**  
> Siber güvenlik artık karmaşık terimlerden ve gri siyah ekranlardan ibaret değil! CyberHealth Desktop, son kullanıcıların günlük dijital güvenliğini koruyan modern, renkli, sade ve %100 gizlilik odaklı bir masaüstü uygulamasıdır.

---

## 🔒 Gizlilik Garantisi (Veri Saklama Politikası)

> **Soru: CyberHealth kişisel verilerimi veya e-postalarımı sunucularda saklıyor mu?**  
> **Cevap: KESİNLİKLE HAYIR.**  
> - **İnternetsiz Yerel Çalışma:** Tüm sezgisel bağlantı analizleri, şifre üretimi ve güvenlik ipuçları bilgisayarınızda yerel olarak çalışır.
> - **Gizlilik Korumalı E-posta Denetimi:** E-posta adresiniz sunuculara asla ham şekilde gönderilmez. SHA-1 özetinin yalnızca ilk 5 karakteri kullanılarak K-Anonymity yöntemiyle sorgulanır.
> - **Yerel Geçmiş:** Taramalarınız harici bir sunucuya gitmez, yalnızca kendi bilgisayarınızda saklanır ve istediğiniz an *Ayarlar > Geçmiş Taramaları Temizle* seçeneğiyle tek tıkla tamamen silinebilir.

---

## 🌟 Öne Çıkan Özellikler

- **🎨 Canlı ve Modern Renkli Tasarım:** Gri ve sıkıcı standart ekranlar yerine HSL/HEX renk paleti ile tasarlanmış modern arayüz.
- **🔗 "Bu Link Güvenli mi?" (Bağlantı ve Sahtecilik Analizi):**
  - Sahte alan adı tespiti (*gogole.com*, *netfIix.com*, *paypaI.com* gibi harf oyunlarını yakalama).
  - Şüpheli yönlendirmeler (@ işareti, IP adresi kullanımı, güvensiz HTTP, yüksek riskli uzantılar).
  - **İsteğe Bağlı Bulut Gücü:** VirusTotal anahtarınızı ekleyerek taramayı 90'dan fazla bulut motoru ile güçlendirebilirsiniz.
- **✉️ E-posta Sızıntı Kontrolü:**
  - Gizlilik koruma mantığıyla e-postanızın geçmiş veri sızıntılarında yer alıp almadığını sorgular.
  - 4 adımlı çözüm ve güvenlik tavsiyesi sunar.
- **🔑 Akılda Kalıcı ve Güvenli Şifre Üretici:**
  - Unutulan karmaşık semboller yerine kolayca ezberlenebilir **"Parolacık"** (*Örn: Güneşli-Mavi-Ejderha-782*) üretir.
  - Şifre gücü ve tahmini kırılma süresi hesaplar.
- **🌐 Kürtçe, Türkçe ve İngilizce Çoklu Dil ve Tema Desteği:**
  - Varsayılan dil olarak **Kürtçe** entegre edilmiştir. Tek tıkla canlı dil ve Karanlık/Aydınlık mod değişimi yapılabilir.

---

## 🚀 Çalıştırma Talimatları

### 1. Doğrudan Python ile Çalıştırma

```bash
pip install -r requirements.txt
python main.py
```

### 2. Derlenmiş Uygulama Oluşturma

```bash
python build.py
```

Derlenen uygulama `dist/CyberHealthDesktop` klasörü içerisinde hazır olacaktır.

---

## 🛠️ Teknolojiler

- **Programlama Dili:** Python 3.10+
- **Kullanıcı Arayüzü:** CustomTkinter
- **Veri ve Ağ İşlemleri:** urllib, re, requests, hashlib, secrets

---

## 📝 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Özgürce kullanabilir, geliştirebilir ve paylaşabilirsiniz.
