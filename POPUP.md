# Reusable Popup Yapısı Kullanım Kılavuzu

Bu projede, popup pencereleri tamamen yeniden kullanılabilir (reusable) ve modüler bir şekilde tasarlanmıştır. Aşağıda popup sisteminin mimarisi, layout kullanımı, sayfa oluşturma ve routing ile ilgili tüm teknik detaylar ve örnekler yer almaktadır.

---

## 1. Popup Layout ve Bileşenleri

Ana popup iskeleti `templates/components/popup.html` dosyasında tanımlıdır. Bu layout, tüm popup'lar için temel bir çerçeve sunar:

- **popup-overlay:** Arka planı karartan katman.
- **popup:** Popup içeriğini saran ana kutu.
- **popup__top:** Kapatma butonu.
- **popup__content:** Dinamik olarak doldurulan içerik alanı (form, bilgi, vs.).
- **popup__bottom:** "İptal" ve "Kaydet" butonları.

Bu yapı, farklı içeriklerle tekrar tekrar kullanılabilir.

---

## 2. Popup İçeriği Oluşturma

Her popup için ayrı bir içerik şablonu hazırlanır. Örneğin:
- `popup_sport_create.html`: Spor dalı ekleme formu
- `popup_facility_create.html`: Tesis ekleme formu

Bu içerik şablonları, popup'ın ana gövdesine dinamik olarak yüklenir.

---

## 3. Routing: Popup İçeriği Sunmak

Popup içerikleri için Flask'ta özel route'lar tanımlanır. Örneğin:

```python
@app.route('/popup/sport_create')
def popup_sport_create():
    return render_template('components/popup_sport_create.html')
```

Her popup için benzer şekilde bir route oluşturulur. Bu route, sadece popup içeriğini döner.

---

## 4. JavaScript ile Popup Açmak

Popup'lar, `static/js/popup.js` dosyasındaki fonksiyonlarla açılır:

- `openPopup(contentHtml, onSave)`: HTML içeriğiyle popup açar.
- `openPopupUrl(url, onSave)`: Bir URL'den (ör. Flask route) içerik çekip popup olarak gösterir.

Kapatma, iptal ve kaydetme işlemleri otomatik olarak yönetilir.

---

## 5. Kullanım Akışı ve Örnek

### Adım 1: Popup İçeriği Oluştur
`templates/components/popup_sport_create.html`:
```html
<form id="add-sport-form">
  <div class="form__group">
    <label for="sport-name">Spor Dalı Adı</label>
    <input type="text" id="sport-name" name="sport_name" class="form__input" required>
  </div>
</form>
```

### Adım 2: Routing Tanımla
`app.py`:
```python
@app.route('/popup/sport_create')
def popup_sport_create():
    return render_template('components/popup_sport_create.html')
```

### Adım 3: Popup'ı Açmak için JS Kullan
```js
// Bir butona tıklandığında popup aç:
document.getElementById('add-sport-btn').onclick = function() {
  openPopupUrl('/popup/sport_create', function(overlay) {
    const form = overlay.querySelector('#add-sport-form');
    const name = form.sport_name.value.trim();
    // AJAX ile sunucuya gönder, başarılıysa popup'ı kapat
  });
};
```

---

## 6. Genişletilebilirlik ve En İyi Pratikler
- Yeni bir popup eklemek için sadece yeni bir içerik şablonu ve route eklemeniz yeterli.
- Aynı JS fonksiyonları ile tüm popup'lar açılabilir.
- Popup içeriği ister form, ister bilgi kutusu, ister onay penceresi olabilir.
- Tasarım ve davranış tek bir merkezden yönetildiği için bakım ve geliştirme çok kolaydır.

---

**Özet:**
Popup sistemi, layout + içerik + routing + JS ile tamamen reusable ve modülerdir. Her türlü popup ihtiyacınız için kolayca genişletilebilir ve özelleştirilebilir.
