
try {
    new Function("import('/reactfiles/frontend/main.6d0ef47e.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.6d0ef47e.js';
    el.type = 'module';
    document.body.appendChild(el);
}
