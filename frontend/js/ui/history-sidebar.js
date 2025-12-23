import State from '../state.js';

const HistorySidebar = (function () {
  const container = document.getElementById('history-list');

  function render(history) {
    if (!container) return;
    container.innerHTML = '';
    history.forEach((item, i) => {
      const el = document.createElement('div');
      el.className = 'history-item';
      el.textContent = item.slice(0, 120);
      el.title = item;
      el.addEventListener('click', () => {
        // ask LineManager to load
        const ev = new CustomEvent('history:load', { detail: item });
        window.dispatchEvent(ev);
      });
      container.appendChild(el);
    });
  }

  function init() {
    render(State.get('queryHistory') || []);
    State.subscribe('queryHistory', render);
  }

  return { init };
})();

export default HistorySidebar;
