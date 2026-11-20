// The moving cover: one function of time. window.__fab(t) draws second t, window.__len is the length.
const NS = 'http://www.w3.org/2000/svg', root = document.getElementById('root');
const SC = 210 / 104, R_RING = 356, R_MON = 384, R_LAB = 236, BG = '#0E0B09';
const INK = DATA.ink, BRASS = DATA.brass, TERRA = DATA.terra;
function el(tag, at, par) { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); (par || root).appendChild(e); return e; }
const rad = a => (a - 90) * Math.PI / 180;                       // a: degrees clockwise from the top
const pt = (r, a) => [r * Math.cos(rad(a)), r * Math.sin(rad(a))];
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ss = u => { u = clamp(u); return u * u * (3 - 2 * u); };
const back = u => { u = clamp(u); const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const dayAng = d => d / 365 * 360;
function arcPath(r, a0, a1) { const [x0, y0] = pt(r, a0), [x1, y1] = pt(r, a1); return `M${x0.toFixed(2)},${y0.toFixed(2)} A${r},${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1.toFixed(2)},${y1.toFixed(2)}`; }

// ---- the year: a thread round the lotus, one arc a month ----
const GAP = 1.1, base = [], prog = [], mlab = [], mmid = [];
for (let m = 0; m < 12; m++) {
  const a0 = dayAng(DATA.mstart[m]) + GAP, a1 = dayAng(DATA.mstart[m + 1]) - GAP;
  base.push(el('path', { d: arcPath(R_RING, a0, a1), fill: 'none', stroke: BRASS, 'stroke-width': 1.6, opacity: .34 }));
  prog.push(el('path', { d: '', fill: 'none', stroke: BRASS, 'stroke-width': 2.8, 'stroke-linecap': 'round' }));
  const mid = (DATA.mstart[m] + DATA.mstart[m + 1]) / 2; mmid.push(mid); const th = rad(dayAng(mid)), [x, y] = pt(R_RING + 17 + 25 * Math.abs(Math.cos(th)) + 8 * Math.abs(Math.sin(th)), dayAng(mid));   // the same gap from the thread all the way round
  const tx = el('text', { x: x.toFixed(1), y: (y + 5.5).toFixed(1), 'text-anchor': 'middle', 'font-family': 'Inter', 'font-weight': 600, 'font-size': 15.5, 'letter-spacing': 2.8, fill: BRASS }); tx.textContent = DATA.mon[m]; mlab.push(tx);
}
el('circle', { r: 107.5 * SC, fill: 'none', stroke: BRASS, 'stroke-width': 1, opacity: .3 });

// ---- the lotus: twelve rooms, twelve petals; room 12 at the top, room 1 at one o'clock ----
const glow = {}, fillp = {}, vein = {}, pulse = {}, rlab = {};
for (let h = 1; h <= 12; h++) {
  const g = el('g', { transform: `rotate(${h * 30}) scale(${SC})` }), col = DATA.aim[(h - 1) % 4];
  el('path', { d: DATA.petal, fill: col, 'fill-opacity': .11, stroke: BRASS, 'stroke-width': .7, 'stroke-opacity': .5 }, g);
  glow[h] = el('path', { d: DATA.petal, fill: col, opacity: 0, filter: 'url(#blur)' }, g);
  fillp[h] = el('path', { d: DATA.petal, fill: col, 'fill-opacity': 0 }, g);
  vein[h] = el('path', { d: 'M0,-58 L0,-93', stroke: '#FFFDF8', 'stroke-width': .7, 'stroke-opacity': 0, 'stroke-linecap': 'round' }, g);
  pulse[h] = el('path', { d: DATA.petal, fill: 'none', stroke: TERRA, 'stroke-width': 2.2, 'stroke-linejoin': 'round', opacity: 0 }, g);
}
for (let h = 0; h < 12; h++) el('path', { d: DATA.innerp, transform: `rotate(${h * 30 + 15}) scale(${SC})`, fill: 'rgba(255,240,214,.09)', stroke: BRASS, 'stroke-width': .6, 'stroke-opacity': .6 });
for (let h = 1; h <= 12; h++) {
  const a = h * 30 * Math.PI / 180, sx = Math.sin(a), cy = -Math.cos(a);
  const tx = el('text', { x: (R_LAB * sx).toFixed(1), y: (R_LAB * cy + (cy > .5 ? 24 : cy < -.5 ? -4 : 10)).toFixed(1), 'text-anchor': Math.abs(sx) < .3 ? 'middle' : sx > 0 ? 'start' : 'end',
    'font-family': 'Cormorant Garamond', 'font-weight': 600, 'font-size': 30, fill: INK }); tx.textContent = DATA.short[h]; rlab[h] = tx;
}

// ---- the grahas of the sky, each on its own path through the petals ----
const orbs = {};
for (const g of ['Mercury', 'Venus', 'Sun', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu']) {
  const [r, rr] = DATA.orb[g], G = el('g', {});
  el('circle', { r: rr * 1.9, fill: DATA.gc[g], opacity: .36, filter: 'url(#soft)' }, G);
  const ring = el('circle', { r: rr, fill: 'none', stroke: TERRA, 'stroke-width': 2.4, opacity: 0 }, G);
  el('circle', { r: rr, fill: `url(#g${g})`, stroke: 'rgba(255,253,248,.72)', 'stroke-width': 1.1 }, G);
  orbs[g] = { G, r, rr, ring };
}

// ---- the middle: the date ----
el('circle', { r: 77, fill: '#15100C', stroke: BRASS, 'stroke-width': 1.8 });
el('circle', { r: 69, fill: 'none', stroke: BRASS, 'stroke-width': 1, 'stroke-dasharray': '2 5', opacity: .5 });
const dateT = el('text', { y: 5, 'text-anchor': 'middle', 'font-family': 'Cormorant Garamond', 'font-weight': 600, 'font-size': 41, fill: INK });
const yearT = el('text', { x: 2, y: 30, 'text-anchor': 'middle', 'font-family': 'Inter', 'font-weight': 600, 'font-size': 12.5, 'letter-spacing': 4, fill: BRASS }); yearT.textContent = DATA.year;

// ---- eclipses (small open beads) and the exact meetings (the beads that stay) ----
const ecl = DATA.ecl.map(d => { const [x, y] = pt(R_RING, dayAng(d)); return { d, c: el('circle', { cx: x.toFixed(1), cy: y.toFixed(1), r: 4.6, fill: BG, stroke: BRASS, 'stroke-width': 1.6 }) }; });
const keys = DATA.keys.map(k => {
  const a = dayAng(k.day), [x, y] = pt(R_RING, a), G = el('g', { transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})` });
  const rip = el('circle', { r: 8, fill: 'none', stroke: TERRA, 'stroke-width': 2, opacity: 0 }, G);
  el('circle', { r: 7, fill: BG, stroke: TERRA, 'stroke-width': 2, opacity: .85 }, G);
  const dot = el('circle', { r: 10, fill: TERRA, stroke: BG, 'stroke-width': 2.6, transform: 'scale(0)' }, G);
  const [lx, ly] = pt(R_RING + 30, a), mid = Math.abs(lx) < 130;
  const lab = el('text', { x: (lx + (mid ? 0 : lx > 0 ? -4 : 4)).toFixed(1), y: (ly + (ly > 300 ? 22 : 10)).toFixed(1), 'text-anchor': mid ? 'middle' : lx > 0 ? 'start' : 'end', 'font-family': 'Cormorant Garamond', 'font-weight': 600, 'font-size': 31, fill: INK, opacity: 0 }); lab.textContent = k.label;
  let month = -1; for (let m = 0; m < 12; m++) if (Math.abs(mmid[m] - k.day) < 9) month = m;
  return Object.assign({}, k, { rip, dot, lab, month });
});
const travG = el('g', {}); el('circle', { r: 19, fill: TERRA, opacity: .55, filter: 'url(#soft)' }, travG); el('circle', { r: 8.5, fill: '#FFF3DF', stroke: TERRA, 'stroke-width': 2.6 }, travG);

window.__len = DATA.len;
window.__fab = function (t) {
  t = clamp(t, 0, DATA.len); const kf = DATA.kf; let d = 364;
  for (let k = 0; k < kf.length - 1; k++) if (t >= kf[k][0] && t <= kf[k + 1][0]) { d = kf[k][1] + (kf[k + 1][1] - kf[k][1]) * ss((t - kf[k][0]) / ((kf[k + 1][0] - kf[k][0]) || 1)); break; }
  const i = Math.min(364, Math.floor(d)), j = Math.min(364, i + 1), f = d - i;
  // petals: the rooms both slow grahas point at open, and close again when the sky moves on
  const meet = {}; let dwell = 0;
  for (const k of keys) { const e = ss((t - k.t0) / .2) * (1 - ss((t - k.t1) / 1.2)); for (const h of k.houses) meet[h] = Math.max(meet[h] || 0, e); if (t >= k.t0 - .04 && t <= k.t1 + .12) dwell = 1; }
  for (let h = 1; h <= 12; h++) {
    const tone = DATA.lit[i][h] * (1 - f) + DATA.lit[j][h] * f, e = ss(tone);
    fillp[h].setAttribute('fill-opacity', (.94 * e).toFixed(3)); glow[h].setAttribute('opacity', (.55 * e).toFixed(3)); vein[h].setAttribute('stroke-opacity', (.42 * e).toFixed(3));
    pulse[h].setAttribute('opacity', (meet[h] || 0).toFixed(3)); rlab[h].setAttribute('opacity', (.5 + .5 * Math.max(e, meet[h] || 0)).toFixed(3));
  }
  // the sky
  for (const g in orbs) {
    const o = orbs[g], a0 = DATA.ang[g][i], a1 = DATA.ang[g][j], a = a0 + ((((a1 - a0) % 360) + 540) % 360 - 180) * f, [x, y] = pt(o.r, a);
    o.G.setAttribute('transform', `translate(${x.toFixed(2)} ${y.toFixed(2)})`); let op = 0, rr = o.rr;
    for (const k of keys) if (k.walkers.includes(g) && t >= k.t0 && t <= k.t1 + .5) { const ph = ((t - k.t0) * 1.5) % 1; rr = o.rr + 3 + 17 * ph; op = (1 - ph) * (1 - ss((t - k.t1) / .5)); }
    o.ring.setAttribute('r', rr.toFixed(2)); o.ring.setAttribute('opacity', op.toFixed(3));
  }
  // the thread of the year
  for (let m = 0; m < 12; m++) {
    const s = DATA.mstart[m], e = DATA.mstart[m + 1], a0 = dayAng(s) + GAP, a1 = Math.min(dayAng(e) - GAP, dayAng(d));
    prog[m].setAttribute('d', a1 > a0 + .05 ? arcPath(R_RING, a0, a1) : '');
    const w = ss(1 - Math.abs(d - mmid[m]) / 22); let hide = 0; for (const k of keys) if (k.month === m) hide = ss((t - k.t0 - .05) / .3);
    mlab[m].setAttribute('opacity', ((.5 + .5 * w) * (1 - hide)).toFixed(3)); mlab[m].setAttribute('fill', w > .5 ? INK : BRASS);
  }
  for (const e of ecl) { const on = d >= e.d; e.c.setAttribute('fill', on ? BRASS : BG); e.c.setAttribute('opacity', on ? 1 : .6); }
  for (const k of keys) {
    const u = (t - k.t0) / .36; k.dot.setAttribute('transform', `scale(${t < k.t0 ? 0 : back(u).toFixed(3)})`);
    const r = (t - k.t0) / .9; k.rip.setAttribute('r', (8 + 44 * ss(r)).toFixed(1)); k.rip.setAttribute('opacity', t < k.t0 || r > 1 ? 0 : (.9 * (1 - r)).toFixed(3));
    k.lab.setAttribute('opacity', ss((t - k.t0 - .05) / .3).toFixed(3));
  }
  const [tx, ty] = pt(R_RING, dayAng(d)); travG.setAttribute('transform', `translate(${tx.toFixed(2)} ${ty.toFixed(2)})`);
  dateT.textContent = DATA.lab[Math.min(364, Math.round(d))]; dateT.setAttribute('fill', dwell ? TERRA : INK);
};
window.__fab(0);
