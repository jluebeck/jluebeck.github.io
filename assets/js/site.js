// Sidebar: list the current page's sections and highlight the one in view.
(function () {
  var secs = document.getElementById('secs');
  if (!secs) return;
  var sections = document.querySelectorAll('main section[id][data-title]');
  sections.forEach(function (s) {
    var li = document.createElement('li'), a = document.createElement('a');
    a.href = '#' + s.id; a.textContent = s.dataset.title;
    li.appendChild(a); secs.appendChild(li);
  });
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) secs.querySelectorAll('a').forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
    });
  }, { rootMargin: '-25% 0px -65% 0px' });
  sections.forEach(function (s) { io.observe(s); });
})();
