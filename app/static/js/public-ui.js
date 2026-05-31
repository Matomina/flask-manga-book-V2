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

let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

function updateCartCount() {
  const count = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const badge = document.getElementById('floatingCartCount');

  if (!badge) {
    return;
  }

  badge.textContent = count;
  badge.style.display = count > 0 ? 'flex' : 'none';
}

function renderCart(containerId) {
  const container = document.getElementById(containerId);

  if (!container) {
    return;
  }

  if (!cartItems.length) {
    container.innerHTML = '<div class="empty-cart"><p>Votre panier est vide</p></div>';
    return;
  }

  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  container.innerHTML = `${cartItems
    .map(
      (item) => `
      <div class="cart-item">
        <img src="${item.img}" alt="${item.name}">
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          <div class="cart-qty">
            <button type="button" data-cart-action="decrease" data-name="${item.name}">−</button>
            <span>${item.quantity}</span>
            <button type="button" data-cart-action="increase" data-name="${item.name}">+</button>
          </div>
        </div>
        <span class="cart-price">${(item.price * item.quantity).toFixed(2)}€</span>
      </div>
    `,
    )
    .join('')}
    <div class="cart-total"><strong>Total : ${subtotal.toFixed(2)}€</strong></div>`;
}

function renderAllCarts() {
  renderCart('cartContent');
  renderCart('cartPageContent');
}

function saveCart() {
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
  renderAllCarts();
  updateCartCount();
}

function addToCart(name, price, img, btn = null) {
  if (!name || Number.isNaN(price)) {
    return;
  }

  const existing = cartItems.find((item) => item.name === name);

  if (existing) {
    existing.quantity += 1;
  } else {
    cartItems.push({ name, price, quantity: 1, img });
  }

  saveCart();

  if (btn) {
    const original = btn.textContent;
    btn.textContent = 'Ajouté';
    setTimeout(() => {
      btn.textContent = original;
    }, 1500);
  }
}

function updateQuantity(name, change) {
  const item = cartItems.find((cartItem) => cartItem.name === name);

  if (!item) {
    return;
  }

  item.quantity = Math.max(0, item.quantity + change);

  if (item.quantity === 0) {
    cartItems = cartItems.filter((cartItem) => cartItem.name !== name);
  }

  saveCart();
}

function openCartPopup() {
  document.body.classList.add('no-scroll');
  document.getElementById('cartPopup')?.classList.add('active');
  document.getElementById('cartOverlay')?.classList.add('active');
  renderCart('cartContent');
}

function closeCartPopup() {
  document.body.classList.remove('no-scroll');
  document.getElementById('cartPopup')?.classList.remove('active');
  document.getElementById('cartOverlay')?.classList.remove('active');
}

function quickCheckout() {
  if (!cartItems.length) {
    alert('Votre panier est vide.');
    return;
  }

  alert('Merci pour votre commande !');
  cartItems = [];
  localStorage.removeItem('cartItems');
  saveCart();
  closeCartPopup();
}

function initCartButtons() {
  document.querySelectorAll('.add-to-cart-btn').forEach((btn) => {
    btn.addEventListener('click', (event) => {
      if (!btn.dataset.title) {
        return;
      }

      event.preventDefault();
      addToCart(
        btn.dataset.title,
        Number.parseFloat(btn.dataset.price),
        btn.dataset.img,
        btn,
      );
    });
  });

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-cart-action]');

    if (!target) {
      return;
    }

    const change = target.dataset.cartAction === 'increase' ? 1 : -1;
    updateQuantity(target.dataset.name, change);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initScroll('.scroll-container', '.card-list');
  initCartButtons();

  onEvent(document.getElementById('floatingCartBtn'), 'click', openCartPopup);
  onEvent(document.getElementById('cartOverlay'), 'click', closeCartPopup);
  onEvent(document.getElementById('cartCloseBtn'), 'click', closeCartPopup);
  onEvent(document.getElementById('quickCheckoutBtn'), 'click', quickCheckout);
  onEvent(document.getElementById('cartPageCheckoutBtn'), 'click', quickCheckout);

  renderAllCarts();
  updateCartCount();
});
