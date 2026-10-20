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
