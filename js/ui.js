/* ALFATAH UI — hero slideshow, drawers, PDP gallery, shop filters. */
(function () {
  "use strict";

  /* ---------------- drawers ---------------- */

  var scrim = document.querySelector("[data-scrim]");

  function closeDrawers() {
    document.querySelectorAll("[data-drawer]").forEach(function (d) {
      d.dataset.open = "false";
      d.setAttribute("aria-hidden", "true");
    });
    if (scrim) scrim.dataset.open = "false";
    document.body.style.overflow = "";
  }

  function openDrawer(name) {
    var drawer = document.querySelector('[data-drawer="' + name + '"]');
    if (!drawer) return;
    closeDrawers();
    drawer.dataset.open = "true";
    drawer.setAttribute("aria-hidden", "false");
    if (scrim) scrim.dataset.open = "true";
    document.body.style.overflow = "hidden";
    var focusable = drawer.querySelector("input, button, a");
    if (focusable) focusable.focus();
  }

  document.addEventListener("click", function (ev) {
    var opener = ev.target.closest("[data-drawer-open]");
    if (opener) {
      openDrawer(opener.dataset.drawerOpen);
      return;
    }
    if (ev.target.closest("[data-drawer-close]") || ev.target.closest("[data-scrim]")) {
      closeDrawers();
      return;
    }
    // adding from anywhere but inside the cart drawer opens the cart
    if (ev.target.closest("[data-add]")) {
      var inCart = ev.target.closest('[data-drawer="cart"]');
      if (!inCart) setTimeout(function () { openDrawer("cart"); }, 120);
    }
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") closeDrawers();
  });

  /* ---------------- hero slideshow ---------------- */

  var hero = document.querySelector("[data-hero]");
  if (hero) {
    var slides = hero.querySelectorAll("[data-slide]");
    var dots = hero.querySelectorAll("[data-dot]");
    var index = 0;
    var timer;

    function show(next) {
      index = (next + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.dataset.active = String(n === index); });
      dots.forEach(function (d, n) { d.setAttribute("aria-selected", String(n === index)); });
    }

    function start() {
      if (slides.length < 2) return;
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      stop();
      timer = setInterval(function () { show(index + 1); }, 6500);
    }

    function stop() { clearInterval(timer); }

    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        show(parseInt(dot.dataset.dot, 10));
        start();
      });
    });

    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", start);
    start();
  }

  /* ---------------- PDP gallery + qty ---------------- */

  var pdpMain = document.querySelector("[data-pdp-main]");
  if (pdpMain) {
    document.querySelectorAll("[data-thumb]").forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        pdpMain.src = thumb.dataset.thumb;
        document.querySelectorAll("[data-thumb]").forEach(function (t) {
          t.setAttribute("aria-selected", String(t === thumb));
        });
      });
    });
  }

  document.querySelectorAll("[data-qty]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var input = document.querySelector("[data-qty-input]");
      if (!input) return;
      var next = (parseInt(input.value, 10) || 1) + parseInt(btn.dataset.qty, 10);
      input.value = Math.min(99, Math.max(1, next));
    });
  });

  /* ---------------- shop filters ---------------- */

  var grid = document.querySelector("[data-shop-grid]");
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll("[data-card]"));
    var order = cards.slice();
    var countEl = document.querySelector("[data-result-count]");
    var noResults = document.querySelector("[data-no-results]");
    var sortEl = document.querySelector("[data-sort]");
    var query = new URLSearchParams(location.search);

    // deep links: ?category=Home+%26+Garden and ?q=tahini from the search drawer
    var preset = query.get("category");
    if (preset) {
      document.querySelectorAll('[data-filter="category"]').forEach(function (box) {
        if (box.value === preset) box.checked = true;
      });
    }
    var search = (query.get("q") || "").trim().toLowerCase();

    function selected(kind) {
      return Array.prototype.slice
        .call(document.querySelectorAll('[data-filter="' + kind + '"]:checked'))
        .map(function (b) { return b.value; });
    }

    function apply() {
      var cats = selected("category");
      var brands = selected("brand");
      var shown = 0;

      cards.forEach(function (card) {
        var okCat = !cats.length || cats.indexOf(card.dataset.category) > -1;
        var okBrand = !brands.length || brands.indexOf(card.dataset.brand) > -1;
        var okSearch = !search || card.dataset.name.indexOf(search) > -1 ||
          card.dataset.brand.toLowerCase().indexOf(search) > -1;
        var visible = okCat && okBrand && okSearch;
        card.hidden = !visible;
        if (visible) shown += 1;
      });

      if (countEl) countEl.textContent = shown + (shown === 1 ? " product" : " products");
      if (noResults) noResults.hidden = shown !== 0;
    }

    function sort(mode) {
      var list = order.slice();
      if (mode === "price-asc") {
        list.sort(function (a, b) { return a.dataset.price - b.dataset.price; });
      } else if (mode === "price-desc") {
        list.sort(function (a, b) { return b.dataset.price - a.dataset.price; });
      } else if (mode === "name") {
        list.sort(function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); });
      }
      list.forEach(function (card) { grid.appendChild(card); });
    }

    document.querySelectorAll("[data-filter]").forEach(function (box) {
      box.addEventListener("change", apply);
    });

    var clear = document.querySelector("[data-clear-filters]");
    if (clear) {
      clear.addEventListener("click", function () {
        document.querySelectorAll("[data-filter]").forEach(function (b) { b.checked = false; });
        search = "";
        apply();
      });
    }

    if (sortEl) sortEl.addEventListener("change", function () { sort(sortEl.value); });

    apply();
  }

  /* ---------------- newsletter ---------------- */

  document.querySelectorAll("[data-newsletter]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var el = document.querySelector("[data-toast]");
      form.reset();
      if (!el) return;
      el.textContent = "Thanks — demo store, nothing was sent.";
      el.dataset.show = "true";
      setTimeout(function () { el.dataset.show = "false"; }, 2600);
    });
  });
})();
