// Simple symbol-pad wiring: finds buttons with `data-latex` and inserts
// at focused textarea (or appends to the last line).

const SymbolPad = (function () {
  function init() {
    document.querySelectorAll('.symbol-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.disabled) return;
        const latex = btn.getAttribute('data-latex') || '';
        // insert into focused textarea or into the last line
        const active = document.activeElement;
        if (active && active.tagName === 'TEXTAREA' && active.classList.contains('line-text')) {
          const start = active.selectionStart || active.value.length;
          const v = active.value;
          active.value = v.slice(0, start) + latex + v.slice(active.selectionEnd || start);
          active.selectionStart = active.selectionEnd = start + latex.length;
          active.focus();
        } else {
          // fallback: append to last line
          const lines = document.querySelectorAll('.line-text');
          if (lines.length) {
            const last = lines[lines.length-1];
            last.value = last.value + latex;
            last.focus();
          }
        }
      });
    });
  }

  return { init };
})();

export default SymbolPad;
