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

function csrfHeaders() {
  return {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
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
        ${item.image ? `<img src="${item.image}" alt="${item.name}">` : ''}
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          <div class="cart-qty">
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

document.addEventListener('DOMContentLoaded', () => {
  initScroll('.scroll-container', '.card-list');
  initCartButtons();
  initPublicMenu();
  initStickyHeader();

  onEvent(document.getElementById('floatingCartBtn'), 'click', openCartPopup);
  onEvent(document.getElementById('cartOverlay'), 'click', closeCartPopup);
  onEvent(document.getElementById('cartCloseBtn'), 'click', closeCartPopup);
  onEvent(document.getElementById('quickCheckoutBtn'), 'click', quickCheckout);
  onEvent(document.getElementById('cartPageCheckoutBtn'), 'click', quickCheckout);

  fetchCart();
});
