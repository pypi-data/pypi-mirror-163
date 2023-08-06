
try {
    new Function("import('/reactfiles/frontend/main.8716a62c.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.8716a62c.js';
    el.type = 'module';
    document.body.appendChild(el);
}
