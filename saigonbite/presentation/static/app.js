// SaigonBite progressive enhancement. Every page works without this file.
(function () {
  "use strict";
  var vnd = function (n) { return n.toLocaleString("en-US") + " VND"; };

  // Quantity steppers and the running total on the menu page
  var form = document.querySelector("[data-menu-form]");
  if (form) {
    var count = form.querySelector("[data-count]");
    var subtotal = form.querySelector("[data-subtotal]");
    var update = function () {
      var items = 0, sum = 0;
      form.querySelectorAll("[data-qty]").forEach(function (input) {
        var q = parseInt(input.value, 10);
        var ok = q > 0 && q <= 99;
        input.closest(".item").classList.toggle("chosen", ok);
        if (ok) { items += q; sum += q * parseInt(input.dataset.price, 10); }
      });
      if (count) count.textContent = items === 1 ? "1 item" : items + " items";
      if (subtotal) subtotal.textContent = vnd(sum);
    };
    form.querySelectorAll("[data-step]").forEach(function (btn) {
      btn.hidden = false;
      btn.addEventListener("click", function () {
        var input = btn.parentNode.querySelector("[data-qty]");
        var q = (parseInt(input.value, 10) || 0) + parseInt(btn.dataset.step, 10);
        q = Math.max(0, Math.min(99, q));
        input.value = q === 0 ? "" : String(q);
        update();
      });
    });
    form.addEventListener("input", update);
    var bar = form.querySelector("[data-summary]");
    if (bar) bar.hidden = false;
    update();
  }

  // Ask before buttons that cannot be undone (archive, reject, failed delivery)
  document.querySelectorAll("form[data-confirm]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      if (!window.confirm(f.dataset.confirm)) { e.preventDefault(); e.stopImmediatePropagation(); }
    });
  });

  // Registration: tourist fields only for tourists
  var reg = document.querySelector("[data-customer-type]");
  if (reg) {
    var showTourist = function () {
      var checked = reg.querySelector("input[name=customer_type]:checked");
      reg.querySelectorAll("[data-for=TOURIST]").forEach(function (box) {
        box.hidden = !checked || checked.value !== "TOURIST";
      });
    };
    reg.addEventListener("change", showTourist);
    showTourist();
  }

  // Quote page: the consent fingerprint is bound to the payment choice (BR-10), and the quote was priced
  // before the customer chose how to pay. When the choice differs, fetch the fingerprint of the chosen
  // payment (a quote request writes nothing) and then send the form, so one click is enough and no false
  // "price changed" notice appears. quoted_total stays as shown: a real price change is still caught.
  var pay = document.querySelector("fieldset.payment");
  if (pay && pay.form && pay.form.dataset.requoteUrl) {
    var cform = pay.form;
    cform.addEventListener("submit", function (e) {
      var chosen = cform.querySelector("input[name=payment]:checked");
      if (!chosen || chosen.value === cform.dataset.quotedPayment || cform.dataset.fingerprintReady) return;
      e.preventDefault(); e.stopImmediatePropagation();
      var button = cform.querySelector("button[type=submit]");
      if (button) { button.disabled = true; button.textContent = button.dataset.busy || "Sending..."; }
      var body = new FormData();
      ["csrf_token", "hub_id", "address_id", "voucher_code"].forEach(function (n) { body.append(n, cform.elements[n].value); });
      cform.querySelectorAll("input[type=hidden][name^=qty_]").forEach(function (i) { body.append(i.name, i.value); });
      body.append("payment", chosen.value);
      var send = function () { cform.dataset.fingerprintReady = "1"; cform.submit(); };
      fetch(cform.dataset.requoteUrl, { method: "POST", body: body, credentials: "same-origin" })
        .then(function (r) { return r.text(); })
        .then(function (html) {
          var found = new DOMParser().parseFromString(html, "text/html").querySelector("input[name=quote_fingerprint]");
          if (found) cform.elements.quote_fingerprint.value = found.value;
          send();
        })
        .catch(send);
    });
  }

  // One click is enough: show that the order is being sent (the server also ignores repeats)
  document.querySelectorAll("form[data-once]").forEach(function (f) {
    f.addEventListener("submit", function () {
      var b = f.querySelector("button[type=submit]");
      if (b) {
        window.setTimeout(function () { b.disabled = true; b.textContent = b.dataset.busy || "Sending..."; }, 0);
      }
    });
  });
})();
