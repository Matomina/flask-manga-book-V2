/* ======================================================
   MangaBook V2 — Public interactions
   ====================================================== */

function onEvent(element, event, callback) {
  if (element) {
    element.addEventListener(event, callback);
  }
}

function initScroll(wrapperSelector, containerSelector) {
  document.querySelectorAll(wrapperSelector).forEach((wrapper) => {
    const container = wrapper.querySelector(containerSelector);
    const btnLeft = wrapper.querySelector(".scroll-btn.left");
    const btnRight = wrapper.querySelector(".scroll-btn.right");

    if (!container) {
      return;
    }

    onEvent(btnLeft, "click", () => {
      container.scrollBy({ left: -300, behavior: "smooth" });
    });

    onEvent(btnRight, "click", () => {
      container.scrollBy({ left: 300, behavior: "smooth" });
    });
  });
}

function initBurgerMenu() {
  const burgerMenu = document.querySelector(".burger-menu");
  const burgerIcon = document.getElementById("burger-icon");
  const mobileNav = document.getElementById("mobile-nav");

  if (!burgerMenu || !burgerIcon || !mobileNav) {
    return;
  }

  burgerMenu.addEventListener("click", () => {
    burgerIcon.classList.toggle("open");
    mobileNav.classList.toggle("active");
    document.body.classList.toggle("no-scroll");
  });

  mobileNav.querySelectorAll("a, button").forEach((link) => {
    link.addEventListener("click", () => {
      burgerIcon.classList.remove("open");
      mobileNav.classList.remove("active");
      document.body.classList.remove("no-scroll");
    });
  });
}

function initScrollTop() {
  const btn = document.getElementById("scrollTopBtn");

  if (!btn) {
    return;
  }

  window.addEventListener("scroll", () => {
    btn.classList.toggle("active", window.scrollY > 300);
  });

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

function initDropdowns() {
  const dropdowns = document.querySelectorAll(".dropdown");

  dropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector(".dropdown-toggle");

    if (!toggle) {
      return;
    }

    toggle.addEventListener("click", (event) => {
      event.stopPropagation();
      dropdown.classList.toggle("active");
    });
  });

  document.addEventListener("click", () => {
    dropdowns.forEach((dropdown) => dropdown.classList.remove("active"));
  });
}

let cartItems = JSON.parse(localStorage.getItem("cartItems") || "[]");

function saveCart() {
  localStorage.setItem("cartItems", JSON.stringify(cartItems));
  renderCart("cartContent");
  renderCart("cartPageContent");
  updateCartCount();
}

function updateCartCount() {
  const count = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const badge = document.getElementById("floatingCartCount");

  if (!badge) {
    return;
  }

  badge.textContent = count;
  badge.style.display = count > 0 ? "flex" : "none";
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
    btn.textContent = "Ajouté";
    setTimeout(() => {
      btn.textContent = original;
    }, 1500);
  }
}

function updateQuantity(name, change) {
  const item = cartItems.find((entry) => entry.name === name);

  if (!item) {
    return;
  }

  item.quantity = Math.max(0, item.quantity + change);

  if (item.quantity === 0) {
    cartItems = cartItems.filter((entry) => entry.name !== name);
  }

  saveCart();
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

  container.innerHTML = `
    ${cartItems
      .map(
        (item) => `
        <div class="cart-item">
          <img src="${item.img}" alt="${item.name}">
          <div class="cart-item-info">
            <strong>${item.name}</strong>
            <div class="cart-qty">
              <button type="button" data-cart-name="${item.name}" data-cart-change="-1">−</button>
              <span>${item.quantity}</span>
              <button type="button" data-cart-name="${item.name}" data-cart-change="1">+</button>
            </div>
          </div>
          <span class="cart-price">${(item.price * item.quantity).toFixed(2)}€</span>
        </div>
      `,
      )
      .join("")}
    <div class="cart-total"><strong>Total : ${subtotal.toFixed(2)}€</strong></div>
  `;

  container.querySelectorAll("[data-cart-name]").forEach((button) => {
    button.addEventListener("click", () => {
      updateQuantity(
        button.dataset.cartName,
        Number.parseInt(button.dataset.cartChange, 10),
      );
    });
  });
}

function openCartPopup() {
  document.body.classList.add("no-scroll");
  document.getElementById("cartPopup")?.classList.add("active");
  document.getElementById("cartOverlay")?.classList.add("active");
  renderCart("cartContent");
}

function closeCartPopup() {
  document.body.classList.remove("no-scroll");
  document.getElementById("cartPopup")?.classList.remove("active");
  document.getElementById("cartOverlay")?.classList.remove("active");
}

function initCart() {
  document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      addToCart(
        btn.dataset.title,
        Number.parseFloat(btn.dataset.price),
        btn.dataset.img,
        btn,
      );
    });
  });

  document
    .querySelector(".floating-cart-btn")
    ?.addEventListener("click", openCartPopup);
  document
    .getElementById("cartOverlay")
    ?.addEventListener("click", closeCartPopup);
  document.querySelector(".close-btn")?.addEventListener("click", closeCartPopup);

  document.querySelector(".btn-checkout")?.addEventListener("click", () => {
    if (!cartItems.length) {
      alert("Votre panier est vide.");
      return;
    }

    alert("Merci pour votre commande !");
    cartItems = [];
    localStorage.removeItem("cartItems");
    saveCart();
    closeCartPopup();
  });

  renderCart("cartContent");
  renderCart("cartPageContent");
  updateCartCount();
}

function initFlashAutoHide() {
  const flash = document.getElementById("flashMessage");

  if (!flash) {
    return;
  }

  setTimeout(() => {
    flash.classList.add("hide");
    setTimeout(() => flash.remove(), 500);
  }, 2500);
}

document.addEventListener("DOMContentLoaded", () => {
  initScroll(".scroll-container", ".card-list");
  initScroll(".scroll-wrapper", ".scroll-list");
  initScroll(".planning-grid-wrapper", ".planning-grid");
  initScroll(".no-fixed-day-wrapper", ".card-row");
  initBurgerMenu();
  initScrollTop();
  initDropdowns();
  initCart();
  initFlashAutoHide();
});
