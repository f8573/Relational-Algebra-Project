import API from './api.js';
import State from './state.js';
import LineManager from './editor/line-manager.js';
import SymbolPad from './editor/symbol-pad.js';
import HistorySidebar from './ui/history-sidebar.js';
import ResultsDisplay from './ui/results-display.js';

// Main initializer
window.addEventListener('DOMContentLoaded', () => {
  LineManager.init();
  SymbolPad.init();
  HistorySidebar.init();

  document.getElementById('btn-run')?.addEventListener('click', async () => {
    const lines = LineManager.getAllLines();
    if (!lines.length) return;
    const script = lines.join('; ');
    ResultsDisplay.showSuccess('Running...');
    try {
      const res = await API.runQuery(script);
      if (!res.ok) {
        ResultsDisplay.showError(`Server error: HTTP ${res.status}`)
      } else if (res.error) {
        ResultsDisplay.showError(res.error + ' — ' + (res.raw||''))
      } else if (res.data && res.data.status === 'success') {
        ResultsDisplay.showSuccess(res.data.output || JSON.stringify(res.data));
        State.pushHistory(script);
      } else {
        ResultsDisplay.showError(JSON.stringify(res.data || res));
      }
    } catch (e) {
      ResultsDisplay.showError('Network error: ' + e.message);
    }
  });

  document.getElementById('btn-new-line')?.addEventListener('click', () => {
    // allow LineManager to create lines via its init handler too
    const ev = new Event('add-line'); window.dispatchEvent(ev);
  });

  // load history click -> load into editor
  window.addEventListener('history:load', (e) => {
    LineManager.load(e.detail);
  });
});
