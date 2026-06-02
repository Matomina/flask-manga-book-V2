function onEvent(element, event, callback) {
  if (element) {
    element.addEventListener(event, callback);
  }
}

function initScroll(wrapperSelector, containerSelector) {
  document.querySelectorAll(wrapperSelector).forEach((wrapper) => {
    const container = wrapper.querySelector(containerSelector);
    const btnLeft = wrapper.querySelector('.scroll-btn.left');
    const btnRight = wrapper.querySelector('.scroll-btn.right');

    if (!container) {
      return;
    }

    onEvent(btnLeft, 'click', () => {
      container.scrollBy({ left: -300, behavior: 'smooth' });
    });

    onEvent(btnRight, 'click', () => {
      container.scrollBy({ left: 300, behavior: 'smooth' });
    });
  });
}

let cartState = { items: [], total: 0, count: 0 };

function csrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

function csrfHeaders() {
  return {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRF-Token': csrfToken(),
  };
}

function updateCartCount() {
  const badge = document.getElementById('floatingCartCount');

  if (!badge) {
    return;
  }

  badge.textContent = cartState.count;
  badge.style.display = cartState.count > 0 ? 'flex' : 'none';
}

function money(value) {
  return Number.parseFloat(value || 0).toFixed(2);
}

function renderCart(containerId) {
  const container = document.getElementById(containerId);

  if (!container) {
    return;
  }

  if (!cartState.items.length) {
    container.innerHTML = '<div class="empty-cart"><p>Votre panier est vide</p></div>';
    return;
  }

  container.innerHTML = `${cartState.items
    .map(
      (item) => `
      <div class="cart-item">
        <div class="cart-item-media">
          ${item.image ? `<img src="${item.image}" alt="${item.name}">` : '<div class="cart-item-image-placeholder"></div>'}
          <div class="cart-qty" aria-label="Modifier la quantité">
            <button
              type="button"
              data-cart-action="decrease"
              data-article-id="${item.article_id}"
              data-quantity="${item.quantity}"
            >−</button>
            <span>${item.quantity}</span>
            <button
              type="button"
              data-cart-action="increase"
              data-article-id="${item.article_id}"
              data-quantity="${item.quantity}"
            >+</button>
          </div>
        </div>
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          <span>Quantité : ${item.quantity}</span>
        </div>
        <span class="cart-price">${money(item.price * item.quantity)}€</span>
      </div>
    `,
    )
    .join('')}
    <div class="cart-total"><strong>Total : ${money(cartState.total)}€</strong></div>`;
}

function renderAllCarts() {
  renderCart('cartContent');
  renderCart('cartPageContent');
  updateCartCount();
}

async function fetchCart() {
  try {
    const response = await fetch('/cart/data', {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    });

    if (!response.ok) {
      return;
    }

    cartState = await response.json();
    renderAllCarts();
  } catch (error) {
    console.error('Impossible de charger le panier.', error);
  }
}

async function postCart(url, payload = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: csrfHeaders(),
    body: JSON.stringify(payload),
  });

  if (response.status === 401 || response.redirected) {
    window.location.href = '/auth/login';
    return null;
  }

  const data = await response.json();

  if (!response.ok) {
    alert(data.error || 'Action panier impossible.');
    return null;
  }

  cartState = data;
  renderAllCarts();
  return data;
}

async function addToCart(articleId, btn = null) {
  if (!articleId) {
    return;
  }

  const data = await postCart(`/cart/add/${articleId}`, { quantity: 1 });

  if (data && btn) {
    const original = btn.textContent;
    btn.textContent = 'Ajouté';
    setTimeout(() => {
      btn.textContent = original;
    }, 1500);
  }
}

async function updateQuantity(articleId, nextQuantity) {
  if (!articleId) {
    return;
  }

  if (nextQuantity <= 0) {
    await postCart(`/cart/remove/${articleId}`);
    return;
  }

  await postCart(`/cart/update/${articleId}`, { quantity: nextQuantity });
}

function openCartPopup() {
  document.body.classList.add('no-scroll');
  document.getElementById('cartPopup')?.classList.add('active');
  document.getElementById('cartOverlay')?.classList.add('active');
  fetchCart();
}

function closeCartPopup() {
  document.body.classList.remove('no-scroll');
  document.getElementById('cartPopup')?.classList.remove('active');
  document.getElementById('cartOverlay')?.classList.remove('active');
}

async function quickCheckout() {
  if (!cartState.items.length) {
    alert('Votre panier est vide.');
    return;
  }

  const response = await fetch('/cart/checkout', {
    method: 'POST',
    headers: csrfHeaders(),
    body: JSON.stringify({}),
  });

  const data = await response.json();

  if (!response.ok) {
    alert(data.error || 'Commande impossible.');
    return;
  }

  window.location.href = data.redirect_url;
}

function initCartButtons() {
  document.querySelectorAll('.add-to-cart-btn').forEach((btn) => {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      addToCart(btn.dataset.articleId, btn);
    });
  });

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-cart-action]');

    if (!target) {
      return;
    }

    const currentQuantity = Number.parseInt(target.dataset.quantity || '1', 10);
    const nextQuantity =
      target.dataset.cartAction === 'increase'
        ? currentQuantity + 1
        : currentQuantity - 1;

    updateQuantity(target.dataset.articleId, nextQuantity);
  });
}

function closePublicMenu() {
  const header = document.querySelector('.public-header');
  const toggle = document.getElementById('publicMenuToggle');

  header?.classList.remove('is-menu-open');
  toggle?.setAttribute('aria-expanded', 'false');
}

function initPublicMenu() {
  const header = document.querySelector('.public-header');
  const toggle = document.getElementById('publicMenuToggle');
  const nav = document.getElementById('publicMainNav');

  if (!header || !toggle || !nav) {
    return;
  }

  toggle.addEventListener('click', () => {
    const isOpen = header.classList.toggle('is-menu-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closePublicMenu);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closePublicMenu();
    }
  });
}

function initStickyHeader() {
  const header = document.querySelector('.public-header');

  if (!header) {
    return;
  }

  const syncHeaderState = () => {
    document.body.classList.toggle('is-public-header-scrolled', window.scrollY > 12);
  };

  syncHeaderState();
  window.addEventListener('scroll', syncHeaderState, { passive: true });
}

function createRevealObserver() {
  return new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -7% 0px',
    },
  );
}

function prepareRevealElement(element, observer, delay = 0, extraClass = '') {
  if (!element || element.classList.contains('reveal-on-scroll')) {
    return;
  }

  element.classList.add('reveal-on-scroll');

  if (extraClass) {
    element.classList.add(extraClass);
  }

  element.style.setProperty('--reveal-delay', `${delay}ms`);
  observer.observe(element);
}

function revealImmediately(elements) {
  elements.forEach((element) => {
    element.classList.add('is-visible');
  });
}

function groupCardsByVisualRow(cards) {
  const rowMap = new Map();

  cards.forEach((card) => {
    const rowTop = Math.round(card.offsetTop / 10) * 10;
    const rowCards = rowMap.get(rowTop) || [];
    rowCards.push(card);
    rowMap.set(rowTop, rowCards);
  });

  return Array.from(rowMap.entries())
    .sort(([firstTop], [secondTop]) => firstTop - secondTop)
    .map(([, rowCards]) => rowCards);
}

function initRevealOnScroll() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const stableSelectors = [
    '.public-main > section:not(.catalog-page):not(.goodies-page):not(.planning-page)',
    '.public-main > article',
    '.page-intro:not(.catalog-page__header)',
    '.home-featured',
    '.public-info-card',
    '.article-detail-card',
    '.auth-card',
    '.forum-topic-card',
  ].join(',');

  const stableElements = Array.from(document.querySelectorAll(stableSelectors)).filter(
    (element) => !element.closest('.public-header, .public-footer, .cart-popup'),
  );

  const carouselSections = Array.from(
    document.querySelectorAll(
      '.planning-list > .planning-day, .goodies-section-list > .goodies-section',
    ),
  ).filter((section) => section.querySelector('.scroll-container'));

  const catalogSupportElements = Array.from(
    document.querySelectorAll(
      '.catalog-page__header, .catalog-search, .catalog-results__header, .goodies-results__header, .planning-page__header, .planning-page__topbar, .goodies-page__header, .goodies-page__topbar',
    ),
  );

  const catalogCards = Array.from(
    document.querySelectorAll('.catalog-results .article-grid > .article-card'),
  );

  const revealElements = [
    ...stableElements,
    ...catalogSupportElements,
    ...carouselSections,
    ...catalogCards,
  ];

  if (!revealElements.length) {
    return;
  }

  if (!('IntersectionObserver' in window)) {
    revealImmediately(revealElements);
    return;
  }

  const observer = createRevealObserver();

  stableElements.forEach((element, index) => {
    prepareRevealElement(element, observer, Math.min(index % 4, 3) * 120);
  });

  catalogSupportElements.forEach((element, index) => {
    prepareRevealElement(element, observer, index * 110);
  });

  carouselSections.forEach((section, index) => {
    prepareRevealElement(section, observer, Math.min(index % 5, 4) * 160, 'reveal-carousel');
  });

  groupCardsByVisualRow(catalogCards).forEach((rowCards, rowIndex) => {
    rowCards.forEach((card) => {
      prepareRevealElement(card, observer, Math.min(rowIndex, 5) * 170, 'reveal-row-card');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initScroll('.scroll-container', '.card-list');
  initCartButtons();
  initPublicMenu();
  initStickyHeader();
  window.requestAnimationFrame(initRevealOnScroll);

  onEvent(document.getElementById('floatingCartBtn'), 'click', openCartPopup);
  onEvent(document.getElementById('cartOverlay'), 'click', closeCartPopup);
  onEvent(document.getElementById('cartCloseBtn'), 'click', closeCartPopup);
  onEvent(document.getElementById('quickCheckoutBtn'), 'click', quickCheckout);
  onEvent(document.getElementById('cartPageCheckoutBtn'), 'click', quickCheckout);

  fetchCart();
});
