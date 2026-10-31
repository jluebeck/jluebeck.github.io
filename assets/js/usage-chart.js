/* Cumulative samples analysed with AmpliconArchitect in published studies.
   UsageChart(container, studies, {height, compact, external}) draws a step-area chart with a hover tooltip.
   Colors come from the page's CSS custom properties: --chart-line, --chart-grid, --chart-text, --chart-ink, --chart-surface. */
function UsageChart(el, all, opts) {
  opts = opts || {};
  var NS = 'http://www.w3.org/2000/svg';
  var fmt = function (n) { return n.toLocaleString('en-US'); };
  var day = function (s) { return new Date(s + 'T00:00:00Z').getTime(); };
  var mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  // The x axis runs from 2017 to the end of the current year; the line extends to today.
  var now = new Date(), lastT = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  var endYear = Math.max(now.getUTCFullYear(), +all[all.length - 1].date.slice(0, 4));
  var t0 = day('2017-01-01'), t1 = Date.UTC(endYear, 11, 31);
  lastT = Math.max(lastT, day(all[all.length - 1].date));
  el.style.position = 'relative';
  var svg = document.createElementNS(NS, 'svg'), tip = document.createElement('div');
  svg.setAttribute('role', 'img'); svg.style.display = 'block'; svg.style.width = '100%'; svg.style.overflow = 'visible';
  tip.className = 'uc-tip'; tip.hidden = true;
  el.appendChild(svg); el.appendChild(tip);

  function draw() {
    var rows = all.filter(function (s) { return !opts.external || s.external; });
    var cum = 0, pts = rows.map(function (s) { cum += s.samples; return { s: s, t: day(s.date), c: cum }; });
    var W = el.clientWidth || 600, H = opts.height || 220, L = opts.compact ? 0 : 44, R = opts.compact ? 0 : 64, T = 14, B = opts.compact ? 0 : 26;
    var top = Math.max(10000, Math.ceil(cum / 20000) * 20000);
    var X = function (t) { return L + (t - t0) / (t1 - t0) * (W - L - R); };
    var Y = function (v) { return T + (1 - v / top) * (H - T - B); };
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('height', H);
    svg.setAttribute('aria-label', 'Cumulative samples analysed with AmpliconArchitect in ' + rows.length + ' published studies, reaching ' + fmt(cum) + ' by ' + (rows.length ? rows[rows.length - 1].date.slice(0, 4) : ''));
    svg.innerHTML = '';
    function el2(n, a, txt) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; svg.appendChild(e); return e; }
    if (!opts.compact) {
      for (var v = 0; v <= top; v += top / (top > 40000 ? 3 : 2)) {
        el2('line', { x1: L, x2: W - R, y1: Y(v), y2: Y(v), stroke: 'var(--chart-grid)', 'stroke-width': 1 });
        el2('text', { x: L - 8, y: Y(v) + 4, 'text-anchor': 'end', fill: 'var(--chart-text)', 'font-size': 11, style: 'font-variant-numeric: tabular-nums' }, v ? (v / 1000) + 'k' : '0');
      }
      var years = []; for (var y = endYear; y >= 2018; y -= 2) years.push(y);
      years.forEach(function (y) { el2('text', { x: X(day(y + '-01-01')), y: H - 6, 'text-anchor': 'middle', fill: 'var(--chart-text)', 'font-size': 11 }, y); });
    }
    if (!pts.length) return;
    var d = 'M' + X(t0) + ' ' + Y(0);
    pts.forEach(function (p) { d += ' H' + X(p.t).toFixed(1) + ' V' + Y(p.c).toFixed(1); });
    d += ' H' + X(lastT).toFixed(1);
    el2('path', { d: d + ' V' + Y(0) + ' Z', fill: 'var(--chart-line)', 'fill-opacity': 0.1, stroke: 'none' });
    el2('path', { d: d, fill: 'none', stroke: 'var(--chart-line)', 'stroke-width': 2, 'stroke-linejoin': 'round' });
    var end = pts[pts.length - 1];
    el2('circle', { cx: X(lastT), cy: Y(end.c), r: 4, fill: 'var(--chart-line)', stroke: 'var(--chart-surface)', 'stroke-width': 2 });
    if (!opts.compact) {
      el2('text', { x: X(lastT) + 8, y: Y(end.c) + 4, fill: 'var(--chart-ink)', 'font-size': 12, 'font-weight': 600, style: 'font-variant-numeric: tabular-nums' }, fmt(end.c));
      var big = pts.reduce(function (a, p) { return p.s.samples > a.s.samples ? p : a; });
      if (big.s.samples > cum * 0.15) {
        el2('text', { x: X(big.t) - 6, y: Y(big.c) + 14, 'text-anchor': 'end', fill: 'var(--chart-text)', 'font-size': 11 }, big.s.citation.split(',')[0] + ', ' + fmt(big.s.samples));
      }
    }
    var cross = el2('line', { y1: T, y2: H - B, stroke: 'var(--chart-text)', 'stroke-width': 1, 'stroke-dasharray': '2 3', visibility: 'hidden' });
    var dot = el2('circle', { r: 4.5, fill: 'var(--chart-line)', stroke: 'var(--chart-surface)', 'stroke-width': 2, visibility: 'hidden' });
    var hit = el2('rect', { x: L, y: 0, width: W - L - R, height: H, fill: 'transparent' });
    function show(ev) {
      var r = svg.getBoundingClientRect(), mx = (ev.clientX - r.left) * (W / r.width), best = pts[0];
      pts.forEach(function (p) { if (Math.abs(X(p.t) - mx) < Math.abs(X(best.t) - mx)) best = p; });
      var px = X(best.t), py = Y(best.c), dt = new Date(best.t);
      cross.setAttribute('x1', px); cross.setAttribute('x2', px); cross.setAttribute('visibility', 'visible');
      dot.setAttribute('cx', px); dot.setAttribute('cy', py); dot.setAttribute('visibility', 'visible');
      tip.innerHTML = '<b></b><span></span><span class="uc-n"></span>';
      tip.children[0].textContent = best.s.label;
      tip.children[1].textContent = best.s.citation + ' · ' + mon[dt.getUTCMonth()] + ' ' + dt.getUTCFullYear();
      tip.children[2].textContent = '+' + fmt(best.s.samples) + ' samples · ' + fmt(best.c) + ' total';
      tip.hidden = false;
      var left = px * (r.width / W), tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, left - tw / 2)) + 'px';
      tip.style.top = Math.max(0, py * (r.height / H) - tip.offsetHeight - 12) + 'px';
    }
    function hide() { tip.hidden = true; cross.setAttribute('visibility', 'hidden'); dot.setAttribute('visibility', 'hidden'); }
    hit.addEventListener('pointermove', show); hit.addEventListener('pointerdown', show); hit.addEventListener('pointerleave', hide);
  }
  draw();
  if ('ResizeObserver' in window) new ResizeObserver(function () { draw(); }).observe(el);
  return { set: function (o) { for (var k in o) opts[k] = o[k]; draw(); } };
}
