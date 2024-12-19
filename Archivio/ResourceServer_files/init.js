ready(init);

function init() {
  var STORAGE_KEY = 'idp-tab';
  var TAB_SELECTOR = 'button[id^="auth-"][id$="-tab"]';

  applyFragments(document.documentElement.dataset.page);
  addFormsSubmitCheck();
  createPopovers();
  randomizeSpidProviders();

  // Tutti i link del footer si aprono in una finestra nuova
  document.querySelectorAll('.idp-footer .idp-link a:not([target])').forEach((el) => el.setAttribute('target', '_blank'));

  // Gestion preferred tabs
  function getTabId(value) {
    value = String(value || '');
    return value.trim().replace(/^auth-|-tab$/g, '');
  }
  function getTabButton(value) {
    return document.getElementById('auth-' + getTabId(value) + '-tab');
  }

  // [SDPRAU-10555] (Teams/Edge18) in caso Bootstrap js non sia caricato
  function activateTab(id) {
    id = getTabId(id);
    document.querySelectorAll('[id^=auth]').forEach((el) => {
      var elId = getTabId(el.id);
      if (elId) {
        el.classList.toggle('active', elId === id);
        if (!el.id.endsWith('-tab')) el.classList.toggle('show', elId === id);
      }
    });
  }

  // Aggiungo un listener ai bottoni che visualizzano i tab
  document.querySelectorAll(TAB_SELECTOR).forEach((button) => {
    button.addEventListener('click', (event) => {
      var tabId = getTabId(event.target.id);
      if (IdpTabsRemember) localStorage.setItem(STORAGE_KEY, tabId);
      sessionStorage.setItem(STORAGE_KEY, tabId);
      // [SDPRAU-10555] (Teams/Edge18) in caso Bootstrap js non sia caricato
      if (typeof bootstrap === 'undefined') activateTab(tabId);
    });
  });

  // Se la gestione non è abilitata, rimuovo dallo storage il tab eventualmente presente
  if (!IdpTabsRemember) {
    localStorage.removeItem(STORAGE_KEY);
  }

  // Determino il tab iniziale
  // Elenco degli id da usare, in ordine decrescente di priorità
  var list = [];
  // Il tab della sessione corrente
  list.push(sessionStorage.getItem(STORAGE_KEY));
  // Il tab dell'ultima visita alla pagina
  list.push(localStorage.getItem(STORAGE_KEY));
  // Il tab indicato nei settings
  list.push(...IdpTabsDefault.split(','));
  // Dopo aver riordinato i tab, il primo già attivo ...
  var tabActive = document.querySelector(TAB_SELECTOR + '.active');
  if (tabActive) list.push(tabActive.id);
  // ... o il primo in assoluto
  var tabFirst = document.querySelector(TAB_SELECTOR);
  if (tabFirst) list.push(tabFirst.id);
  // Trovo il primo bottone valido
  var button = null;
  list.forEach((id) => {
    button = button || getTabButton(id);
  });
  // Simulo la pressione del bottone
  if (button) button.click();

  if (IdpTriggerExternal) {
    triggerButtonExternal(IdpTriggerExternal);
  }
}

// Disabilita il submit delle form specificate se ci sono campi non validi
function addFormsSubmitCheck(selector) {
  // Recupero tutte le form interessate
  document.querySelectorAll(selector || '.needs-validation').forEach((form) => {
    function checkIsValid(event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }
    form.addEventListener('submit', checkIsValid, false);
  });
}

// Riordino casualmente i provider Spid
function randomizeSpidProviders() {
  var rootList = document.querySelector('#spid-idp-list-small-root-get');
  var idpList = rootList ? Array.from(rootList.querySelectorAll('.spid-idp-button-link')) : [];
  while (idpList.length) {
    rootList.insertBefore(idpList.splice(Math.floor(Math.random() * idpList.length), 1)[0], rootList.firstElementChild);
  }
}

// Applica frammenti di html (template) alla pagina
// Il nome specificato determina i frammenti da usare
function applyFragments(name) {
  var insert = (nodes, parent, before) => nodes.forEach((node) => parent.insertBefore(node, before));
  var split = (s) => (s || '').split(/\s+/).filter((t) => t.length);
  document.querySelectorAll(`template[data-fragment]:not([data-applied])`).forEach((template) => {
    var names = String(template.dataset.fragment || '').split(',');
    names = names.map((s) => s.trim()).filter((s) => s);
    if (!(names.includes('*') || (name && names.includes(name)) || (!name && !names.length))) return;
    var targets = template.dataset.target ? document.querySelectorAll(template.dataset.target) : [];
    if (!targets.length) return;
    template.dataset.applied = '';
    var sel = template.dataset.source;
    var sources = sel ? Array.from(document.querySelectorAll(sel)) : [template.content];
    var addClass = split(template.dataset.addClass);
    var removeClass = split(template.dataset.removeClass);
    var addStyle = (template.dataset.addStyle || '').trim().replace(/^;+/, '');
    targets.forEach((target, index) => {
      if (removeClass.length) target.classList.remove(...removeClass);
      if (addClass.length) target.classList.add(...addClass);
      if (addStyle) {
        var style = (target.getAttribute('style') || '').trim().replace(/;+$/, '');
        target.setAttribute('style', style ? style + ';' + addStyle : addStyle);
      }
      var nodes = index > 0 || !sel ? sources.map((el) => el.cloneNode(true)) : sources;
      switch (template.dataset.mode) {
        case 'after-children':
        case 'append':
          return void insert(nodes, target, null);
        case 'before-children':
        case 'insert':
          return void insert(nodes, target, target.firstChild);
        case 'before':
          return void insert(nodes, target.parentNode, target);
        case 'after':
          return void insert(nodes, target.parentNode, target.nextSibling);
        case 'replace':
          insert(nodes, target.parentNode, target);
          return void target.remove();
        case 'remove':
          return void target.remove();
        case 'replace-children':
        case 'content':
          target.textContent = '';
          return void insert(nodes, target, null);
      }
    });
  });
}

// Crea i popover definiti nella pagina
function createPopovers() {
  document.querySelectorAll('[data-bs-toggle="popover"]').forEach((el) => {
    // Crea l'istanza solo se non è già stata creata
    if (!bootstrap.Popover.getInstance(el)) {
      var config = {};
      ['title', 'content'].forEach((name) => {
        var o = el.querySelector(`[data-popover-${name}]`);
        if (o) {
          config.html = true;
          config[name] = o.innerHTML;
        }
      });
      // Mantiene title, se presente
      var title = config.title && el.getAttribute('title');
      var instance = new bootstrap.Popover(el, config);
      if (title) el.setAttribute('title', title);
      el.addEventListener('inserted.bs.popover', function () {
        var arr = Array.from(instance.tip.querySelectorAll('.popover-dismiss'));
        if (instance.tip.classList.contains('popover-dismiss')) arr.push(instance.tip);
        arr.forEach((el) => el.addEventListener('click', () => instance.hide()));
      });
    }
  });
}

function togglePasswordVisibility(event) {
  var parent = event.target.closest('.input-group');
  var input = parent.querySelector('#password');
  var showPassword = input.type === 'password';
  input.type = showPassword ? 'text' : 'password';
  parent.querySelector('#show_eye').classList.toggle('d-none', showPassword);
  parent.querySelector('#hide_eye').classList.toggle('d-none', !showPassword);
}

function redirect(url, delay) {
  if (url == '' || url == '#') return;
  delay = Math.min(20, Math.max(0, parseInt(delay)));
  if (isNaN(delay)) delay = 5;
  const el = document.querySelector('.redirect-countdown');
  if (el) el.textContent = delay;
  if (delay > 0) setTimeout(() => redirect(url, delay - 1), 1000);
  else window.location.href = url;
}
