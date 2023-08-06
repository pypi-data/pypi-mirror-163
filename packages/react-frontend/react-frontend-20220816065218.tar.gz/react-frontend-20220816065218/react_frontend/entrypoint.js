
try {
    new Function("import('/reactfiles/frontend/main.6cec01bc.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.6cec01bc.js';
    el.type = 'module';
    document.body.appendChild(el);
}
