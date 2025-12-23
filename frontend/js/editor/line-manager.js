// Manages editor "lines". Each line is currently a simple textarea
// placeholder for MathQuill fields. Replace internals with MathQuill
// wiring in `mathquill-setup.js` when ready.

const LineManager = (function () {
  const container = document.getElementById('lines-container');
  const lines = [];

  function createLine(initial = '') {
    const wrapper = document.createElement('div');
    wrapper.className = 'line-row';
    const ta = document.createElement('textarea');
    ta.className = 'line-text';
    ta.value = initial;
    wrapper.appendChild(ta);

    const removeBtn = document.createElement('button');
    removeBtn.textContent = '✖';
    removeBtn.className = 'line-remove';
    removeBtn.addEventListener('click', () => {
      container.removeChild(wrapper);
      const idx = lines.indexOf(ta);
      if (idx >= 0) lines.splice(idx, 1);
    });
    wrapper.appendChild(removeBtn);

    container.appendChild(wrapper);
    lines.push(ta);
    ta.focus();
    return ta;
  }

  return {
    init() {
      // ensure at least one line exists
      if (!container) return;
      if (container.children.length === 0) createLine('');
      document.getElementById('btn-new-line')?.addEventListener('click', () => createLine(''));
    },
    getAllLines() {
      return lines.map(t => t.value.trim()).filter(Boolean);
    },
    clear() {
      lines.slice().forEach(t => t.value = '');
    },
    load(text) {
      // naive: clear and add single line
      container.innerHTML = '';
      lines.length = 0;
      createLine(text || '');
    }
  };
})();

export default LineManager;
