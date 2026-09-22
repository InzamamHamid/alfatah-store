/* ALFATAH cart — localStorage only, no backend.
 *
 * State shape:  [{ slug, qty }]   — prices always re-read from data/products.json
 * so a price change in the catalogue never leaves a stale amount in a basket.
 */
(function () {
  "use strict";

  var KEY = "alfatah.cart.v1";
  var BASE = document.body.dataset.base || "";
  var CURRENCY = "QAR";
  var catalogue = {};

  /* ---------------- storage ---------------- */

  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(raw) ? raw.filter(function (l) { return l && l.slug && l.qty > 0; }) : [];
    } catch (err) {
      return [];
    }
  }

  function save(lines) {
    try {
      localStorage.setItem(KEY, JSON.stringify(lines));
    } catch (err) {
      /* private mode / quota — the cart stays in memory for this page only */
    }
    render();
  }

  /* ---------------- money ---------------- */

  function money(value) {
    return CURRENCY + " " + value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function subtotal(lines) {
    return lines.reduce(function (sum, line) {
      var product = catalogue[line.slug];
      return product ? sum + product.price * line.qty : sum;
    }, 0);
  }

  /*
   * TODO(you): delivery charge rule.
   *
   * The captured Elevare store advertised free delivery over a threshold and a
   * flat fee below it, but the real numbers were never exposed to the front end
   * — the header banner is the only clue, and it currently says QAR 250.
   *
   * This is a genuine business decision, not boilerplate, and it changes how the
   * page behaves: a high threshold pushes basket size but makes small orders feel
   * punitive; a low one converts better but eats margin on single-item orders.
   * You may also want a middle tier, or free delivery on a first order.
   *
   * Return the delivery charge in QAR for the given subtotal. Whatever you
   * return here is what the cart drawer, the cart page and the announcement bar
   * threshold should agree on — if you change the threshold, update the
   * `money(250)` in build.py's header() and page_about() FAQ too.
   *
   * @param {number} sub  — order subtotal in QAR
   * @returns {number}    — delivery charge in QAR (0 = free)
   */
  function deliveryFor(sub) {
    // 5-10 lines. Replace this placeholder with the rule you want.
    return sub >= 250 ? 0 : 25;
  }

  function totals() {
    var lines = read();
    var sub = subtotal(lines);
    var delivery = deliveryFor(sub);
    return { lines: lines, sub: sub, delivery: delivery, grand: sub + delivery };
  }

  /* ---------------- mutations ---------------- */

  function add(slug, qty) {
    var lines = read();
    var existing = lines.filter(function (l) { return l.slug === slug; })[0];
    if (existing) {
      existing.qty = Math.min(99, existing.qty + (qty || 1));
    } else {
      lines.push({ slug: slug, qty: qty || 1 });
    }
    save(lines);
    toast((catalogue[slug] ? catalogue[slug].name : "Item") + " added to cart");
  }

  function setQty(slug, qty) {
    var lines = read()
      .map(function (l) { return l.slug === slug ? { slug: slug, qty: qty } : l; })
      .filter(function (l) { return l.qty > 0; });
    save(lines);
  }

  function remove(slug) {
    save(read().filter(function (l) { return l.slug !== slug; }));
  }

  /* ---------------- rendering ---------------- */

  function lineHTML(line) {
    var p = catalogue[line.slug];
    if (!p) return "";
    return (
      '<div class="cart-line" data-line="' + p.slug + '">' +
        '<a class="cart-line__media" href="' + BASE + "products/" + p.slug + '.html">' +
          '<img src="' + BASE + p.image + '" alt="" loading="lazy" width="120" height="120"></a>' +
        "<div>" +
          '<p class="cart-line__brand">' + p.brand + "</p>" +
          '<p class="cart-line__name"><a href="' + BASE + "products/" + p.slug + '.html">' + p.name + "</a></p>" +
          '<div class="qty" style="margin-top:.5rem">' +
            '<button type="button" data-line-qty="-1" aria-label="Decrease quantity">&minus;</button>' +
            "<input type='number' value='" + line.qty + "' min='1' max='99' data-line-input aria-label='Quantity'>" +
            '<button type="button" data-line-qty="1" aria-label="Increase quantity">+</button>' +
          "</div>" +
        "</div>" +
        '<div style="text-align:right;display:grid;gap:.4rem;align-content:start">' +
          "<strong>" + money(p.price * line.qty) + "</strong>" +
          '<button class="cart-line__remove" type="button" data-line-remove>Remove</button>' +
        "</div>" +
      "</div>"
    );
  }

  function totalsHTML(t) {
    return (
      '<div class="totals__row"><span>Subtotal</span><span>' + money(t.sub) + "</span></div>" +
      '<div class="totals__row"><span>Delivery</span><span>' +
        (t.delivery === 0 ? "Free" : money(t.delivery)) + "</span></div>" +
      '<div class="totals__row totals__row--grand"><span>Total</span><span>' + money(t.grand) + "</span></div>"
    );
  }

  function render() {
    var t = totals();
    var count = t.lines.reduce(function (n, l) { return n + l.qty; }, 0);

    document.querySelectorAll("[data-cart-count]").forEach(function (el) {
      el.textContent = count;
      el.hidden = count === 0;
    });

    var empty =
      '<div class="empty"><p>Your cart is empty.</p>' +
      '<a class="btn btn--outline" href="' + BASE + 'shop.html">Start shopping</a></div>';
    var body = t.lines.map(lineHTML).join("");

    var drawerBody = document.querySelector("[data-cart-body]");
    if (drawerBody) drawerBody.innerHTML = count ? body : empty;

    var foot = document.querySelector("[data-cart-foot]");
    if (foot) foot.hidden = count === 0;

    var page = document.querySelector("[data-cart-page]");
    if (page) page.innerHTML = count ? body : empty;

    document.querySelectorAll("[data-cart-totals]").forEach(function (el) {
      el.innerHTML = totalsHTML(t);
    });
  }

  /* ---------------- toast ---------------- */

  var toastTimer;
  function toast(message) {
    var el = document.querySelector("[data-toast]");
    if (!el) return;
    el.textContent = message;
    el.dataset.show = "true";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.dataset.show = "false"; }, 2600);
  }

  /* ---------------- events ---------------- */

  document.addEventListener("click", function (ev) {
    var addBtn = ev.target.closest("[data-add]");
    if (addBtn) {
      var qty = 1;
      if (addBtn.hasAttribute("data-use-qty")) {
        var input = document.querySelector("[data-qty-input]");
        qty = Math.max(1, parseInt(input && input.value, 10) || 1);
      }
      add(addBtn.dataset.add, qty);
      return;
    }

    var lineEl = ev.target.closest("[data-line]");
    if (lineEl) {
      var slug = lineEl.dataset.line;
      var current = read().filter(function (l) { return l.slug === slug; })[0];
      if (!current) return;
      if (ev.target.closest("[data-line-remove]")) {
        remove(slug);
      } else {
        var step = ev.target.closest("[data-line-qty]");
        if (step) setQty(slug, Math.min(99, Math.max(0, current.qty + parseInt(step.dataset.lineQty, 10))));
      }
      return;
    }

    if (ev.target.closest("[data-checkout]")) {
      var t = totals();
      toast(t.lines.length ? "Demo store — checkout ends here. Total " + money(t.grand) : "Your cart is empty.");
    }
  });

  document.addEventListener("change", function (ev) {
    var input = ev.target.closest("[data-line-input]");
    if (!input) return;
    var slug = input.closest("[data-line]").dataset.line;
    setQty(slug, Math.min(99, Math.max(1, parseInt(input.value, 10) || 1)));
  });

  /* ---------------- boot ---------------- */

  fetch(BASE + "data/products.json")
    .then(function (r) { return r.json(); })
    .then(function (list) {
      list.forEach(function (p) { catalogue[p.slug] = p; });
      render();
    })
    .catch(function () { render(); });

  window.AlfatahCart = { add: add, remove: remove, totals: totals, render: render };
})();
