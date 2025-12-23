// Placeholder MathQuill setup. If MathQuill is available on the page
// this module should initialize and export helpers to get/set latex.

const MathQuillSetup = (function () {
  let enabled = false;
  try {
    if (window.MathQuill) enabled = true;
  } catch (e) {}

  function isEnabled() { return enabled; }

  // stub: when MathQuill is present, return the Latex content of the field
  function getLatexFromField(el) {
    if (!enabled) return el.value || el.textContent || '';
    try { return MathQuill.getInterface(2).MathField(el).latex(); } catch (e) { return '' }
  }

  return { isEnabled, getLatexFromField };
})();

export default MathQuillSetup;
