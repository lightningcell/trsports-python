// Popup açma (HTML string ile)
function openPopup(contentHtml, onSave) {
    closePopup();
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    overlay.innerHTML = `
      <div class="popup">
        <div class="popup__top">
          <button class="popup__close" aria-label="Kapat"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="popup__content">${contentHtml}</div>
        <div class="popup__bottom">
          <button class="popup__button popup__button--cancel">İptal</button>
          <button class="popup__button popup__button--save">Kaydet</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    overlay.querySelector('.popup__close').onclick = closePopup;
    overlay.querySelector('.popup__button--cancel').onclick = closePopup;
    overlay.onclick = function(e) {
      if (e.target === overlay) closePopup();
    };
    overlay.querySelector('.popup__button--save').onclick = function() {
      if (typeof onSave === 'function') onSave(overlay);
    };
}
// Popup açma (URL ile, AJAX)
async function openPopupUrl(url, onSave) {
    closePopup();
    const resp = await fetch(url);
    const html = await resp.text();
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    overlay.innerHTML = `
      <div class="popup">
        <div class="popup__top">
          <button class="popup__close" aria-label="Kapat"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="popup__content">${html}</div>
        <div class="popup__bottom">
          <button class="popup__button popup__button--cancel">İptal</button>
          <button class="popup__button popup__button--save">Kaydet</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    // Çalıştırılmamış script taglerini yakala ve çalıştır
    const contentDiv = overlay.querySelector('.popup__content');
    contentDiv.querySelectorAll('script').forEach(oldScript => {
        const newScript = document.createElement('script');
        if (oldScript.src) newScript.src = oldScript.src;
        else newScript.textContent = oldScript.innerHTML;
        document.body.appendChild(newScript);
        oldScript.remove();
    });
    // Kapatma ve save işlemleri
    overlay.querySelector('.popup__close').onclick = closePopup;
    overlay.querySelector('.popup__button--cancel').onclick = closePopup;
    overlay.onclick = function(e) { if (e.target === overlay) closePopup(); };
    overlay.querySelector('.popup__button--save').onclick = function() {
        if (typeof onSave === 'function') onSave(overlay);
    };
}
function closePopup() {
    const old = document.querySelector('.popup-overlay');
    if (old) old.remove();
}
// window.openPopup ve closePopup global olsun
window.openPopup = openPopup;
window.openPopupUrl = openPopupUrl;
window.closePopup = closePopup;
