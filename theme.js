(function () {
  var KEY = "apic-theme";
  var stored = localStorage.getItem(KEY);
  if (stored) document.documentElement.setAttribute("data-theme", stored);

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector("[data-theme-toggle]");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme");
      var isLight = current === "light";
      var next = isLight ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem(KEY, next);
    });
  });
})();
