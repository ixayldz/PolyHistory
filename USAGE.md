# 📖 PolyHistory — Kullanım Kılavuzu

> Sıfırdan üyelik oluşturma, ilk analizinizi başlatma ve tüm platform özelliklerini kullanma rehberi.

---

## İçindekiler

1. [Platforma Genel Bakış](#1-platforma-genel-bakış)
2. [Sistemi Başlatma](#2-sistemi-başlatma)
3. [Hesap Oluşturma (Kayıt)](#3-hesap-oluşturma-kayıt)
4. [Giriş Yapma](#4-giriş-yapma)
5. [Ana Sayfa (Dashboard)](#5-ana-sayfa-dashboard)
6. [Yeni Analiz Oluşturma](#6-yeni-analiz-oluşturma)
7. [Analiz Sonuçlarını İnceleme](#7-analiz-sonuçlarını-i̇nceleme)
8. [Kanıt Paketi (Evidence Pack)](#8-kanıt-paketi-evidence-pack)
9. [Zaman Çizelgesi (Timeline)](#9-zaman-çizelgesi-timeline)
10. [Konsensüs Analizi](#10-konsensüs-analizi)
11. [Rapor Dışa Aktarma](#11-rapor-dışa-aktarma)
12. [Hesap Yönetimi ve Kotalar](#12-hesap-yönetimi-ve-kotalar)
13. [Sık Sorulan Sorular (SSS)](#13-sık-sorulan-sorular-sss)
14. [API ile Kullanım (Geliştiriciler İçin)](#14-api-ile-kullanım-geliştiriciler-i̇çin)

---

## 1. Platforma Genel Bakış

PolyHistory, tarihsel iddiaları **kanıt temelli, çok perspektifli ve çapraz-ulusal** olarak analiz eden bir AI platformudur.

### Ne Yapar?

Bir tarihsel iddia girersiniz — platform şunları otomatik olarak yapar:

```
Sizin Sorunuz
    ↓
┌─────────────────────────────────────────┐
│  1. Önermeyi ayrıştırır (NLP/NER)       │
│  2. Sorguyu 4 dile genişletir           │
│     (Türkçe, İngilizce, Fransızca, Yunanca)│
│  3. Kaynak toplar (arşiv, akademik,     │
│     basın, hatırat)                      │
│  4. Kaynakları puanlar (5 faktörlü      │
│     güvenilirlik formülü)                │
│  5. 3 bağımsız AI modelle analiz eder   │
│     (Gemini, GPT, Claude)               │
│  6. Konsensüs hesaplar                  │
│  7. Şeffaf rapor üretir                 │
└─────────────────────────────────────────┘
    ↓
Denetlenebilir Sonuç + Kanıt Dosyası
```

### Kimler İçin?

| Hedef Kitle | Kullanım Senaryosu |
|------------|-------------------|
| 🎓 Tarih araştırmacıları | Çoklu kaynak doğrulama, farklı perspektif karşılaştırma |
| 📰 Gazeteciler | Tarihsel iddiaların hızlı fact-check'i |
| 🏫 Akademisyenler | Kaynak çeşitliliği denetimi, alıntı doğrulama |
| 👩‍💻 Meraklı kullanıcılar | "Gerçekten öyle mi olmuş?" sorularına kanıtlı cevap |

---

## 2. Sistemi Başlatma

### Ön Gereksinimler

- **Docker Desktop** yüklü ve çalışıyor olmalı
- İnternet bağlantısı

### Adım Adım Kurulum

```bash
# 1. Projeyi indirin
git clone https://github.com/ixayldz/PolyHistory.git
cd PolyHistory

# 2. Ortam dosyasını oluşturun
cp .env.example .env

# 3. (İsteğe bağlı) API anahtarlarınızı ekleyin
#    Not: API anahtarı olmadan da çalışır (fallback modu)
#    .env dosyasını açıp şu değişkenleri doldurun:
#    GEMINI_API_KEY=your-key
#    OPENAI_API_KEY=sk-your-key
#    ANTHROPIC_API_KEY=sk-ant-your-key

# 4. Tüm servisleri başlatın
docker-compose up -d

# 5. Servislerin durumunu kontrol edin
docker-compose ps
```

### Erişim Adresleri

Sistem başlatıldıktan sonra şu adreslerden erişebilirsiniz:

| Servis | Adres | Açıklama |
|--------|-------|----------|
| 🌐 **Web Arayüzü** | http://localhost:3000 | Ana kullanıcı arayüzü |
| 📡 **API** | http://localhost:8000 | Backend API |
| 📖 **API Dokümantasyonu** | http://localhost:8000/docs | Swagger UI |

> **💡 İpucu:** İlk açılışta veritabanı tabloları otomatik oluşturulur. Birkaç saniye bekleyebilir.

---

## 3. Hesap Oluşturma (Kayıt)

### Web Arayüzünden

1. Tarayıcınızda **http://localhost:3000** adresine gidin
2. Sağ üstteki **"Sign Up"** / **"Kayıt Ol"** butonuna tıklayın
3. Formu doldurun:

   | Alan | Açıklama | Gereksinim |
   |------|----------|-----------|
   | **E-posta** | Geçerli bir e-posta adresi | Benzersiz olmalı |
   | **Şifre** | Güvenli bir şifre | En az 8 karakter |

4. **"Register"** butonuna tıklayın
5. ✅ Başarılı! Otomatik olarak giriş sayfasına yönlendirilirsiniz

### API ile (Terminal)

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "benim@email.com",
    "password": "guvenli_sifre_123"
  }'
```

**Başarılı Yanıt:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "benim@email.com",
  "tier": "free",
  "monthly_analysis_count": 0,
  "monthly_analysis_limit": 5
}
```

> **📋 Not:** Tüm yeni hesaplar **Free** tier ile başlar. Free tier ayda **1 çoklu-model** + **4 tekli-model** analiz hakkı sağlar.

---

## 4. Giriş Yapma

### Web Arayüzünden

1. **http://localhost:3000/auth/login** adresine gidin
2. Kayıt olduğunuz e-posta ve şifrenizi girin
3. **"Login"** butonuna tıklayın
4. ✅ Dashboard'a yönlendirilirsiniz

### API ile

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "benim@email.com",
    "password": "guvenli_sifre_123"
  }'
```

**Yanıt:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

> **🔑 Önemli:** `access_token` değerini saklayın — sonraki tüm API isteklerinde kullanacaksınız. Token süresi dolduğunda `refresh_token` ile yenileyebilirsiniz.

### Token Yenileme

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJhbGciOiJIUzI1NiIs..."}'
```

---

## 5. Ana Sayfa (Dashboard)

Giriş yaptıktan sonra ana sayfayı göreceksiniz. Ana sayfa şu bölümlerden oluşur:

### Üst Navigasyon Çubuğu

| Menü | Açıklama |
|------|----------|
| **PolyHistory** | Ana sayfaya dönüş |
| **Cases** | Tüm analizlerinizin listesi |
| **Analytics** | İstatistik ve raporlar |
| **Settings** | Hesap ayarları |
| **Logout** | Çıkış yapma |

### Arama Alanı

Sayfanın ortasında büyük bir arama kutusu bulunur. Buraya tarihsel önermenizi yazacaksınız.

**Örnek önermeler:**

| Dil | Örnek |
|-----|-------|
| 🇹🇷 Türkçe | "Mustafa Kemal Atatürk İngilizlerle gizli bir işbirliği yaptı mı?" |
| 🇹🇷 Türkçe | "Osmanlı'nın çöküşünde dış müdahalenin rolü neydi?" |
| 🇬🇧 İngilizce | "Was the Treaty of Sèvres designed to permanently partition Anatolia?" |
| 🇹🇷 Türkçe | "İstiklal Savaşı'nda Sovyet yardımının kapsamı ne kadardı?" |

### Özellik Kartları

Üç özellik kartı platformun ana yeteneklerini özetler:

| Kart | Açıklama |
|------|----------|
| 🔍 **Multi-Source Research** | Arşiv, akademik yayın ve dönem basınından otomatik kaynak toplama |
| 📊 **AI Consensus** | 3 bağımsız AI modeliyle ağırlıklı konsensüs analizi |
| 📄 **Evidence Hierarchy** | Net kaynak sınıflandırması ve güvenilirlik puanlaması |

### Son Analizler

Sayfanın altında en son yaptığınız analizlerin kısa listesi yer alır.

---

## 6. Yeni Analiz Oluşturma

### Adım 1: Önerme Yazma

Dashboard'daki arama kutusuna sorunuzu yazın. Bazı kurallar:

| Kural | Açıklama |
|-------|----------|
| ✅ Minimum 10 karakter | Çok kısa önermeler kabul edilmez |
| ✅ Belirli bir dönem referansı verin | "1919-1923 arası" gibi |
| ✅ Coğrafi bağlam ekleyin | "Turkey", "UK" gibi |
| ❌ Çok genel sorular sormayın | "Tarih nedir?" → Çok geniş |

### Adım 2: Seçenekler (İsteğe Bağlı)

API üzerinden ek seçenekler belirleyebilirsiniz:

| Seçenek | Açıklama | Varsayılan |
|---------|----------|-----------|
| `time_window` | Tarih aralığı (YYYY-MM-DD) | Otomatik tespit |
| `geography` | İlgili ülkeler listesi | Otomatik tespit |
| `require_steel_man` | En güçlü karşı-argümanı zorunlu kılma | `true` |
| `source_preference` | Kaynak tercihi: `balanced` / `primary_heavy` | `balanced` |
| `languages` | Aranacak diller | `["tr", "en"]` |

### Adım 3: Analizi Başlatma

**Web'de:** "Analyze" butonuna tıklayın.

**API ile:**
```bash
curl -X POST http://localhost:8000/api/v1/cases \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "proposition": "Mustafa Kemal Atatürk İngilizlerle gizli bir işbirliği yaptı mı?",
    "time_window": {
      "start": "1919-05-01",
      "end": "1923-10-29"
    },
    "geography": ["Turkey", "UK"],
    "options": {
      "require_steel_man": true,
      "source_preference": "balanced",
      "languages": ["tr", "en", "fr"]
    }
  }'
```

### Adım 4: Bekleme

Analiz arka planda çalışır. İşlem süresi:

| Mod | Süre | Açıklama |
|-----|------|----------|
| **Çoklu-model** (3 AI) | 30-90 saniye | Gemini + GPT + Claude birlikte |
| **Tekli-model** (1 AI) | 10-30 saniye | Sadece ilk kullanılabilir model |
| **Fallback** (yerel) | 2-5 saniye | AI yoksa deterministik analiz |

Analiz durumunu takip etmek için:

```bash
# Durumu kontrol et
curl http://localhost:8000/api/v1/cases/$CASE_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Durum değerleri:**

| Status | Anlam |
|--------|-------|
| `pending` | Sıraya alındı |
| `processing` | Analiz devam ediyor |
| `completed` | ✅ Tamamlandı — sonuçlar hazır |
| `failed` | ❌ Hata oluştu |

---

## 7. Analiz Sonuçlarını İnceleme

Analiz tamamlandığında aşağıdaki bilgilere erişebilirsiniz:

### Genel Özet

| Alan | Açıklama |
|------|----------|
| **Önerme** | Girdiğiniz tarihsel iddia |
| **Güven Skoru** | 0.0 - 1.0 arası genel güven değeri |
| **Güven Etiketi** | `very_high` / `high` / `medium` / `low` |
| **Kısa Karar** | AI modellerinin ortak sonuç özeti |
| **MBR Uyumluluğu** | Kaynak çeşitliliği yeterli mi? |
| **Analiz Modu** | `multi_model` veya `single_model` |
| **Degradasyon Seviyesi** | `full` / `partial` / `reduced` / `fallback` |

### Güven Skoru Nasıl Hesaplanır?

```
Final Skor = 0.4 × Uzlaşma Oranı + 0.6 × Kanıt Gücü
```

| Etiket | Skor Aralığı | Anlam |
|--------|-------------|-------|
| 🟢 `very_high` | ≥ 0.86 | Güçlü uzlaşma + sağlam kanıt |
| 🔵 `high` | ≥ 0.61 | Tutarlı uzlaşma — temel iddia |
| 🟡 `medium` | ≥ 0.31 | Kısmi uzlaşma — orta güven |
| 🔴 `low` | < 0.31 | Zayıf uzlaşma veya yetersiz kanıt |

### Web'de Sonuçları Görüntüleme

1. Dashboard'da analizinize tıklayın veya **Cases** sayfasına gidin
2. İlgili analiz kartına tıklayın
3. Detay sayfasında tüm bilgileri göreceksiniz

### API ile Sonuçları Çekme

```bash
curl http://localhost:8000/api/v1/cases/$CASE_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Örnek Yanıt:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "proposition": "Mustafa Kemal Atatürk İngilizlerle gizli bir işbirliği yaptı mı?",
  "status": "completed",
  "confidence_score": 0.4823,
  "verdict": {
    "short_statement": "Diplomatik temaslar belgelenmiş olmakla birlikte, gizli işbirliği iddiasını destekleyen birincil kaynak bulunamamıştır."
  },
  "mbr_compliant": true,
  "normalized_proposition": { ... },
  "consensus": { ... }
}
```

---

## 8. Kanıt Paketi (Evidence Pack)

Her analiz için toplanan kaynakları detaylı inceleyebilirsiniz.

### Kaynak Türleri

| Tür | Ağırlık | Açıklama | Örnekler |
|-----|---------|----------|----------|
| 📜 **primary** | 1.0 | Birincil kaynaklar | Resmi belgeler, telgraflar, antlaşma metinleri |
| 📚 **academic** | 0.8 | Akademik yayınlar | Hakemli dergiler, üniversite yayınları |
| 📖 **secondary** | 0.7 | İkincil kaynaklar | Tarih kitapları, ansiklopedi maddeleri |
| 📰 **press** | 0.4 | Dönem basını | Gazete haberleri, dergi makaleleri |
| ✍️ **memoir** | 0.5 | Hatıratlar | Anılar, biyografiler, günlükler |

### Güvenilirlik Puanlama (5 Faktör)

Her kaynak şu formülle puanlanır:

```
Güvenilirlik = 0.30 × Kaynak_Türü
             + 0.25 × Kurum_İtibarı
             + 0.20 × Belge_Kalitesi
             + 0.15 × Çapraz_Kaynak_Tutarlılığı
             + 0.10 × Atıf_Puanı
```

| Faktör | Ağırlık | Açıklama |
|--------|---------|----------|
| **Kaynak Türü** | %30 | Birincil > Akademik > İkincil > Basın |
| **Kurum İtibarı** | %25 | Milli arşivler (0.9) > Üniversite (0.8) > Ticari (0.5) |
| **Belge Kalitesi** | %20 | Dijital doğma = 1.0, OCR taraması = kalite puanı |
| **Tutarlılık** | %15 | Diğer kaynaklarla ne kadar uyumlu |
| **Atıf Puanı** | %10 | Kaynak türüne göre tahmini etki |

### Kaynakları Filtreleme

```bash
# Sadece birincil kaynaklar
curl "http://localhost:8000/api/v1/cases/$CASE_ID/evidence?source_type=primary" \
  -H "Authorization: Bearer $TOKEN"

# Sadece Türk kaynakları
curl "http://localhost:8000/api/v1/cases/$CASE_ID/evidence?country=TR" \
  -H "Authorization: Bearer $TOKEN"

# Karşı görüş kaynakları
curl "http://localhost:8000/api/v1/cases/$CASE_ID/evidence?stance=contra" \
  -H "Authorization: Bearer $TOKEN"
```

### Kanıt Detayları

Her kanıt öğesi şu bilgileri içerir:

| Alan | Açıklama |
|------|----------|
| `title` | Kaynak başlığı |
| `author` | Yazar(lar) |
| `publisher` | Yayıncı |
| `publication_date` | Yayın tarihi |
| `country` | Kaynak ülkesi |
| `language` | Kaynak dili |
| `source_type` | Kaynak türü (primary, academic vb.) |
| `stance` | Tutum (pro / contra / neutral) |
| `reliability_score` | Güvenilirlik puanı (0.0 - 1.0) |
| `reliability_factors` | 5 faktörün ayrı ayrı puanları |
| `snippets` | İlgili metin alıntıları |

---

## 9. Zaman Çizelgesi (Timeline)

Kanıtları zaman ekseninde görselleştirebilirsiniz.

### Granülarlik Seçenekleri

| Değer | Açıklama |
|-------|----------|
| `day` | Günlük bazda |
| `week` | Haftalık bazda |
| `month` | Aylık bazda (varsayılan) |
| `year` | Yıllık bazda |

### API Kullanımı

```bash
# Aylık zaman çizelgesi
curl "http://localhost:8000/api/v1/cases/$CASE_ID/timeline?granularity=month" \
  -H "Authorization: Bearer $TOKEN"
```

**Yanıt:**
```json
[
  {
    "id": "ev-001",
    "date": "1919-05-01",
    "track": "TR_pro",
    "title": "Samsun'a Çıkış Emri",
    "description": "primary source from TR",
    "evidence_type": "primary"
  },
  {
    "id": "ev-002",
    "date": "1919-06-15",
    "track": "UK_neutral",
    "title": "British Cabinet Minutes",
    "description": "primary source from UK",
    "evidence_type": "primary"
  }
]
```

Her olay bir **track** üzerinde gösterilir: `{ülke}_{tutum}` formatında (örn. `TR_pro`, `UK_neutral`).

---

## 10. Konsensüs Analizi

Konsensüs ekranı, AI modellerinin ortak analizini gösterir.

### İddia Kategorileri

İddialar üç gruba ayrılır:

| Kategori | Açıklama | Kriter |
|----------|----------|--------|
| 🟢 **Core Claims** | Temel uzlaşma iddiaları | `very_high` veya `high` güven |
| 🟡 **Medium Claims** | Orta güven iddiaları | `medium` güven |
| 🔴 **Disputed Claims** | Tartışmalı iddialar | Modeller arasında tutum farklılığı |

### Uzlaşma Matrisi (Agreement Matrix)

Hangi modelin hangi iddiayı desteklediğini gösteren bir matris:

```
            │ İddia 1 │ İddia 2 │ İddia 3
────────────┼─────────┼─────────┼─────────
Gemini      │ support │ support │ oppose
GPT         │ support │ neutral │ oppose
Claude      │ support │ oppose  │ support
────────────┼─────────┼─────────┼─────────
Uzlaşma     │  3/3 ✅  │  1/3 ❌  │  2/3 ⚠️
```

### API ile Konsensüs Verisi

```bash
curl http://localhost:8000/api/v1/cases/$CASE_ID/consensus \
  -H "Authorization: Bearer $TOKEN"
```

---

## 11. Rapor Dışa Aktarma

Analiz sonuçlarını dosya olarak indirebilirsiniz.

### Desteklenen Formatlar

| Format | Dosya Türü | Açıklama |
|--------|-----------|----------|
| 📝 **Markdown** | `.md` | Metin bazlı, tüm detaylarla birlikte |
| 📊 **JSON** | `.json` | Programatik erişim için yapılandırılmış veri |
| 📄 **PDF** | `.pdf` | ⏳ Yakında (henüz mevcut değil) |

### Rapor İçeriği

İndirilen rapor şunları içerir:

- Orijinal önerme ve normalize hali
- Tüm kanıtların listesi ve güvenilirlik puanları
- AI modellerinin ayrı ayrı analizleri
- Konsensüs sonuçları ve uzlaşma matrisi
- Tartışmalı noktalar ve belirsizlikler
- Chicago tarzı bibliyografya

### Kullanım

**API ile:**
```bash
# Markdown rapor
curl -X POST http://localhost:8000/api/v1/cases/$CASE_ID/export \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"format": "markdown", "citation_style": "chicago"}' \
  --output rapor.md

# JSON rapor
curl -X POST http://localhost:8000/api/v1/cases/$CASE_ID/export \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"format": "json"}' \
  --output rapor.json
```

---

## 12. Hesap Yönetimi ve Kotalar

### Üyelik Tipleri

| Özellik | Free Tier | Pro Tier |
|---------|-----------|----------|
| **Çoklu-model analiz** | 1 / ay | Sınırsız |
| **Tekli-model analiz** | 4 / ay | — |
| **Toplam analiz** | 5 / ay | Plan kapsamında |
| **AI modeli sayısı** | İlk analiz: 3, sonrakiler: 1 | Her zaman 3 |
| **Dışa aktarma** | ✅ | ✅ |
| **API erişimi** | ✅ | ✅ |

### Çoklu-Model vs Tekli-Model Farkı

| Mod | Açıklama | Güven Tavanı |
|-----|----------|-------------|
| **Çoklu-model** | 3 AI (Gemini + GPT + Claude) birlikte analiz eder | %100 |
| **Tekli-model** | Sadece 1 AI analiz eder | %50 |

> **💡 İpucu:** Free tier'da ilk analiziniz otomatik olarak çoklu-model modunda çalışır. Sonraki 4 analiziniz tekli-model modunda olacaktır. Ay başında kotanız sıfırlanır.

### Kalan Kotanızı Kontrol Etme

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

```json
{
  "id": "...",
  "email": "benim@email.com",
  "tier": "free",
  "monthly_analysis_count": 2,
  "monthly_analysis_limit": 5
}
```

Bu örnekte 2 analiz kullanılmış, 3 analiz hakkı kalmış demektir.

---

## 13. Sık Sorulan Sorular (SSS)

### ❓ API anahtarı olmadan kullanabilir miyim?

**Evet.** PolyHistory, API anahtarları olmadan da çalışır. Bu durumda yerel **fallback modu** devreye girer — deterministik bir analiz üretilir. Ancak 3 AI modelinin tam konsensüsü için en az bir API anahtarı gereklidir.

### ❓ Hangi dillerdeki kaynakları arar?

Platform 4 dilde sorgu genişletmesi yapar:
- 🇹🇷 **Türkçe** — Osmanlıca terimler dahil
- 🇬🇧 **İngilizce** — Dönem terminolojisiyle
- 🇫🇷 **Fransızca** — Osmanlı diplomasi dili
- 🇬🇷 **Yunanca** — Çapraz-ulusal perspektif

### ❓ MBR (Minimum Denge Gereksinimleri) nedir?

Her analiz için zorunlu kaynak çeşitliliği kontrolleri:
- En az 2 Türk kaynağı
- En az 1-2 yabancı ülke kaynağı (konuya göre)
- En az 1 destekleyen ve 1 karşı görüş kaynağı

MBR'yi karşılamayan analizler %20 güven cezası alır.

### ❓ "Degradation" (bozulma seviyesi) ne anlama gelir?

AI modelleri her zaman yanıt vermeyebilir. Platform buna hazırdır:

| Durum | Ne Olur |
|-------|---------|
| 3/3 model başarılı | Normal analiz (tam güven) |
| 2/3 model başarılı | Devam eder (%80 güven tavanı) |
| 1/3 model başarılı | Kısıtlı analiz (%50 tavan) |
| 0/3 model başarılı | Yerel fallback (%40 tavan) |

### ❓ Analizimi silebilir miyim?

**Evet.**

```bash
curl -X DELETE http://localhost:8000/api/v1/cases/$CASE_ID \
  -H "Authorization: Bearer $TOKEN"
```

### ❓ Analiz ne kadar sürer?

- **Çoklu-model:** 30-90 saniye
- **Tekli-model:** 10-30 saniye
- **Fallback:** 2-5 saniye

### ❓ Sonuçlar ne kadar güvenilir?

PolyHistory "kesin doğruyu" söyleme iddiasında değildir. Platform:
- Her iddiayı kanıt referanslarıyla destekler
- Model uyumsuzluklarını şeffaf gösterir
- Belirsizlikleri açıkça listeler
- Kaynakları bağımsız doğrulamanıza olanak tanır

---

## 14. API ile Kullanım (Geliştiriciler İçin)

### Hızlı Referans

Tüm isteklere `Authorization: Bearer $TOKEN` header'ı eklemelisiniz.

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Kayıt | `POST` | `/api/v1/auth/register` |
| Giriş | `POST` | `/api/v1/auth/login` |
| Token yenileme | `POST` | `/api/v1/auth/refresh` |
| Profil | `GET` | `/api/v1/auth/me` |
| Analiz oluştur | `POST` | `/api/v1/cases` |
| Analizleri listele | `GET` | `/api/v1/cases` |
| Analiz detayı | `GET` | `/api/v1/cases/{id}` |
| Analiz sil | `DELETE` | `/api/v1/cases/{id}` |
| Kanıtlar | `GET` | `/api/v1/cases/{id}/evidence` |
| Zaman çizelgesi | `GET` | `/api/v1/cases/{id}/timeline` |
| Konsensüs | `GET` | `/api/v1/cases/{id}/consensus` |
| Dışa aktar | `POST` | `/api/v1/cases/{id}/export` |

### Tam Kullanım Senaryosu (Uçtan Uca)

```bash
#!/bin/bash
# PolyHistory — Uçtan Uca Analiz Örneği

API="http://localhost:8000/api/v1"

# 1. Giriş yap
echo "🔐 Giriş yapılıyor..."
LOGIN=$(curl -s -X POST $API/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "benim@email.com", "password": "guvenli_sifre_123"}')

TOKEN=$(echo $LOGIN | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
AUTH="Authorization: Bearer $TOKEN"

# 2. Analiz oluştur
echo "📝 Analiz oluşturuluyor..."
CASE=$(curl -s -X POST $API/cases \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "proposition": "İstiklal Savaşı sırasında Sovyet yardımının kapsamı neydi?",
    "time_window": {"start": "1920-01-01", "end": "1922-12-31"},
    "geography": ["Turkey", "Russia"],
    "options": {"require_steel_man": true, "languages": ["tr", "en"]}
  }')

CASE_ID=$(echo $CASE | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
echo "📋 Case ID: $CASE_ID"

# 3. Analiz tamamlanmasını bekle
echo "⏳ Analiz bekleniyor..."
while true; do
  STATUS=$(curl -s $API/cases/$CASE_ID -H "$AUTH" | \
    python3 -c "import sys,json;print(json.load(sys.stdin)['status'])")
  echo "   Durum: $STATUS"
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then break; fi
  sleep 5
done

# 4. Sonuçları al
echo "📊 Sonuçlar:"
curl -s $API/cases/$CASE_ID -H "$AUTH" | python3 -m json.tool

# 5. Kanıtları al
echo "📜 Kanıtlar:"
curl -s "$API/cases/$CASE_ID/evidence" -H "$AUTH" | python3 -m json.tool

# 6. Konsensüsü al
echo "🤝 Konsensüs:"
curl -s "$API/cases/$CASE_ID/consensus" -H "$AUTH" | python3 -m json.tool

# 7. Raporu indir
echo "📥 Rapor indiriliyor..."
curl -s -X POST "$API/cases/$CASE_ID/export" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"format": "markdown", "citation_style": "chicago"}' \
  --output analiz_raporu.md

echo "✅ Tamamlandı! Rapor: analiz_raporu.md"
```

### Swagger UI

Tüm endpoint'leri interaktif olarak denemek için tarayıcınızda açın:

```
http://localhost:8000/docs
```

Swagger UI'da her endpoint için:
- Parametreleri görebilir
- "Try it out" ile doğrudan test edebilir
- Yanıt şemasını inceleyebilirsiniz

---

<p align="center">
  <strong>Sorularınız mı var?</strong><br>
  <a href="https://github.com/ixayldz/PolyHistory/issues">GitHub Issues</a> üzerinden bize ulaşın.
</p>

<p align="center">
  <sub>PolyHistory v2.0.0 — Evidence-First Historical Analysis</sub>
</p>
