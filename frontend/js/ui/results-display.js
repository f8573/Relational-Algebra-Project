const ResultsDisplay = (function () {
  const out = document.getElementById('output') || document.getElementById('output-area');

  function showSuccess(text) {
    if (!out) return;
    out.textContent = text || '(no output)';
    out.classList.remove('error');
  }

  function showError(text) {
    if (!out) return;
    out.textContent = text || 'Error';
    out.classList.add('error');
  }

  return { showSuccess, showError };
})();

export default ResultsDisplay;
