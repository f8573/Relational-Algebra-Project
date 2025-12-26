// Patch: Convert letters inside MathQuill's \mathcal{...} to Unicode mathematical script capitals
// This ensures calligraphic rendering even when fonts don't auto-map glyphs.
(function(){
  const MAP = {
    'A':'\uD835\uDC9C','B':'\uD835\uDC9D','C':'\uD835\uDC9E','D':'\uD835\uDC9F','E':'\uD835\uDCA0','F':'\uD835\uDCA1','G':'\uD835\uDCA2','H':'\uD835\uDCA3','I':'\uD835\uDCA4','J':'\uD835\uDCA5','K':'\uD835\uDCA6','L':'\uD835\uDCA7','M':'\uD835\uDCA8','N':'\uD835\uDCA9','O':'\uD835\uDCAA','P':'\uD835\uDCAB','Q':'\uD835\uDCAC','R':'\uD835\uDCAD','S':'\uD835\uDCAE','T':'\uD835\uDCAF','U':'\uD835\uDCB0','V':'\uD835\uDCB1','W':'\uD835\uDCB2','X':'\uD835\uDCB3','Y':'\uD835\uDCB4','Z':'\uD835\uDCB5'
  }
  function toScriptCaps(str){
    return String(str).replace(/[A-Z]/g, ch => MAP[ch] || ch)
  }
  function transformNode(node){
    if (!node || !node.classList || !node.classList.contains('mq-mathcal')) return
    // Replace text nodes under mq-mathcal with script capital equivalents
    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT)
    let t
    const pending = []
    while ((t = walker.nextNode())){
      const txt = t.nodeValue
      if (/[A-Z]/.test(txt)) pending.push({ t, txt })
    }
    pending.forEach(({t, txt}) => { t.nodeValue = toScriptCaps(txt) })
  }
  function install(){
    const root = document.body
    if (!root) return
    // Initial pass
    document.querySelectorAll('.mq-mathcal').forEach(transformNode)
    // Observe future mutations from MathQuill editing
    const obs = new MutationObserver(muts => {
      for (const m of muts){
        if (m.type === 'childList'){
          m.addedNodes && m.addedNodes.forEach(n => {
            try{ transformNode(n) }catch(e){}
            if (n.querySelectorAll){
              n.querySelectorAll('.mq-mathcal').forEach(transformNode)
            }
          })
        } else if (m.type === 'attributes'){
          try{ transformNode(m.target) }catch(e){}
        }
      }
    })
    obs.observe(root, { childList: true, subtree: true, attributes: true })
  }
  try{
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install)
    else install()
  }catch(e){ /* ignore */ }
})();
