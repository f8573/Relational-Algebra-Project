// Simple state store with event subscription
const State = (function () {
  const listeners = new Map();
  const store = {
    currentUser: null,
    queryHistory: JSON.parse(localStorage.getItem('queryHistory') || '[]'),
    currentAssessmentId: null,
  };

  function notify(key) {
    const fns = listeners.get(key) || [];
    for (const fn of fns) fn(store[key]);
  }

  return {
    get(key) { return store[key]; },
    set(key, value) {
      store[key] = value;
      if (key === 'queryHistory') localStorage.setItem('queryHistory', JSON.stringify(value));
      notify(key);
    },
    subscribe(key, fn) {
      const arr = listeners.get(key) || [];
      arr.push(fn);
      listeners.set(key, arr);
      // return unsubscribe
      return () => {
        const cur = listeners.get(key) || [];
        listeners.set(key, cur.filter(x => x !== fn));
      };
    },
    pushHistory(item) {
      const h = store.queryHistory.slice();
      h.unshift(item);
      if (h.length > 100) h.length = 100;
      this.set('queryHistory', h);
    }
  };
})();

export default State;
