/**
 * Shared utility for /compare/ pages.
 * Each page defines window.COMPARE_CALC = { scenarios, priceTable } before loading this script,
 * or calls initCompare(data) after fetching pricing-data.json.
 */

(function () {
  const $ = id => document.getElementById(id);

  function fmt$(v) {
    if (v === 0) return '$0';
    if (v < 1) return '$' + v.toFixed(2);
    if (v < 10000) return '$' + Math.round(v).toLocaleString('en-US');
    return '$' + Math.round(v).toLocaleString('en-US');
  }

  // Update all [data-price] span elements
  function applyPrices(prices) {
    document.querySelectorAll('[data-price]').forEach(el => {
      const key = el.getAttribute('data-price');
      const val = resolveDot(prices, key);
      if (val !== undefined && val !== null) {
        el.textContent = typeof val === 'number' ? fmt$(val) : val;
      }
    });
  }

  // Resolve dot-notation key from nested object
  function resolveDot(obj, path) {
    return path.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj);
  }

  // Update "Last updated" chip
  function applyLastUpdated(date) {
    const el = $('luDate');
    if (el) el.textContent = date;
  }

  // Run page-specific calc after data loads
  function runCalc(data) {
    applyLastUpdated(data.lastUpdated);
    if (typeof window.onPricingData === 'function') {
      window.onPricingData(data, fmt$);
    }
  }

  // FAQ accordion
  function initFaq() {
    document.querySelectorAll('.qa').forEach(qa => {
      qa.querySelector('.q').addEventListener('click', () => {
        const open = qa.classList.contains('open');
        document.querySelectorAll('.qa').forEach(x => {
          x.classList.remove('open');
          x.querySelector('.a').style.maxHeight = null;
        });
        if (!open) {
          qa.classList.add('open');
          qa.querySelector('.a').style.maxHeight = qa.querySelector('.a').scrollHeight + 'px';
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initFaq();
    fetch('/pricing-data.json')
      .then(r => r.json())
      .then(runCalc)
      .catch(() => {
        // silently fail — fallback values remain in DOM
        if (typeof window.onPricingData === 'function') {
          window.onPricingData(window.PRICING_FALLBACK || {}, fmt$);
        }
      });
  });
})();
