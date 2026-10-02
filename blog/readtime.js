(function () {
  var body = document.querySelector('.post-body');
  var meta = document.querySelector('.meta');
  if (!body || !meta) return;
  var text = body.innerText || body.textContent || '';
  var words = text.trim().split(/\s+/).filter(function (w) { return /\w/.test(w); }).length;
  var mins = Math.max(1, Math.round(words / 200));
  var base = meta.textContent.replace(/\s*·\s*\d+\s*min read\s*$/, '');
  meta.textContent = base + ' · ' + mins + ' min read';
})();
