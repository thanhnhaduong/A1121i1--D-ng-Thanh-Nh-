/* art.js — tranh minh họa phẳng, màu mờ (không viền, không điểm bóng) cho poster tối giản.
   Mỗi tranh vẽ trên khung 520 x 200 và minh họa ĐÚNG những thứ được nhắc trong ý của mục. */
const M = {
  ink: '#2b2f3a', cream: '#fbf6ea', paper: '#f5f0e4', white: '#fffdf7',
  rose: '#c2566b', roseL: '#efbfc0', roseXL: '#f8e3e0',
  mus: '#d99a2b', musD: '#b97f17', musL: '#f1d08a', musXL: '#f9edcf',
  plum: '#7b5ca3', plumL: '#c8b6df', plumXL: '#ece4f2',
  grn: '#3f7d58', grnD: '#2e6044', grnL: '#9ccb9b', grnXL: '#e2efdd',
  blu: '#2e6f9e', bluD: '#245676', bluL: '#9cc4dc', bluXL: '#dfeaf3',
  ter: '#c0603c', terD: '#9a4a2d', terL: '#e7ab90', terXL: '#f8e4da',
  navy: '#233a5c', gray: '#5d6b73', grayL: '#a9b3b8', wood: '#c79a63', woodD: '#a67a46'
};
const rad = d => d * Math.PI / 180;
const T = (x, y, s = 1, rot = 0, inner = '') => `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">${inner}</g>`;
const rect = (x, y, w, h, r, f, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${f}" ${extra}/>`;
const circ = (x, y, r, f, extra = '') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${f}" ${extra}/>`;
const ell = (x, y, rx, ry, f, rot = 0) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${f}" transform="rotate(${rot} ${x} ${y})"/>`;
const path = (d, f, extra = '') => `<path d="${d}" fill="${f}" ${extra}/>`;

function sector(cx, cy, r, a0, a1, fill, gap = 3) {
  const m = rad((a0 + a1) / 2), ox = cx + gap * Math.cos(m), oy = cy + gap * Math.sin(m);
  const p = a => [(ox + r * Math.cos(rad(a))).toFixed(1), (oy + r * Math.sin(rad(a))).toFixed(1)];
  const [x0, y0] = p(a0), [x1, y1] = p(a1);
  return path(`M${ox.toFixed(1)} ${oy.toFixed(1)}L${x0} ${y0}A${r} ${r} 0 ${(a1 - a0) >= 180 ? 1 : 0} 1 ${x1} ${y1}Z`, fill);
}
const BLOB_D = 'M14 104C6 56 56 12 124 14C186 16 236 8 300 16C364 22 430 8 488 30C520 44 518 90 506 130C494 172 440 196 376 192C316 188 270 198 200 194C120 190 24 176 14 104Z';
const blob = (c, o = 1) => path(BLOB_D, c, `opacity="${o}"`);
let _g = 0;
const inBlob = inner => { const id = 'bl' + (++_g); return `<clipPath id="${id}"><path d="${BLOB_D}"/></clipPath><g clip-path="url(#${id})">${inner}</g>`; };

/* ---------- đồ vật dùng chung ---------- */
const bulbG = (lit = true, glow = '#f6d77a') => `${lit ? circ(0, -6, 32, glow, 'opacity=".38"') : ''}
  ${path('M-9 14C-9 7 -20 3 -20 -9A20 20 0 1 1 20 -9C20 3 9 7 9 14Z', lit ? '#f7d77f' : '#e6ecf2')}
  ${rect(-9, 14, 18, 6, 3, M.gray)}${rect(-6.5, 21, 13, 5, 2.5, M.gray)}
  ${path('M-4 12V-1L0 -6L4 -1V12', 'none', 'stroke="#d99a2b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity=".8"')}`;
const heartG = c => path('M0 24C-32 3 -28 -20 -13 -23C-6 -24 -1 -19 0 -15C1 -19 6 -24 13 -23C28 -20 32 3 0 24Z', c);
const leafG = (a, b) => path('M-24 24C-32 -6 -6 -30 26 -28C28 6 4 32 -24 24Z', a) + path('M-24 24C-8 12 12 -6 26 -28C28 6 4 32 -24 24Z', b);
const dropG = (c) => path('M0 -30C0 -30 -22 -4 -22 10A22 22 0 0 0 22 10C22 -4 0 -30 0 -30Z', c);
const sparkG = c => path('M0 -11Q1.6 -1.6 11 0Q1.6 1.6 0 11Q-1.6 1.6 -11 0Q-1.6 -1.6 0 -11Z', c);
const gearG = (c, R = 27, r = 21, n = 8, hole = 8.5) => {
  const s = 2 * Math.PI / n; let d = '';
  for (let i = 0; i < n; i++) {
    const a = i * s;
    [[a - s * .21, r], [a - s * .12, R], [a + s * .12, R], [a + s * .21, r]].forEach(([g, q], j) => {
      d += (i === 0 && j === 0 ? 'M' : 'L') + (q * Math.cos(g)).toFixed(1) + ' ' + (q * Math.sin(g)).toFixed(1) + ' ';
    });
  }
  d += `ZM${hole} 0A${hole} ${hole} 0 1 0 ${-hole} 0A${hole} ${hole} 0 1 0 ${hole} 0Z`;
  return `<path fill-rule="evenodd" d="${d}" fill="${c}"/>`;
};
let _u = 0;
const flaskG = (liq, glass = '#e7f0f3') => {
  const id = 'fk' + (++_u), d = 'M-8 -28H8V-10L26 22Q30 30 22 30H-22Q-30 30 -26 22L-8 -10Z';
  return `<clipPath id="${id}"><path d="${d}"/></clipPath>${path(d, glass)}<g clip-path="url(#${id})">${rect(-32, 6, 64, 30, 0, liq)}</g>${rect(-11, -32, 22, 6, 3, M.gray)}`;
};
const rocketG = (body = M.cream, acc = M.ter) => `
  ${path('M-11 4L-25 28L-11 24Z', acc)}${path('M11 4L25 28L11 24Z', acc)}
  ${path('M-7 26Q0 50 7 26Z', M.mus)}${path('M-3.4 26Q0 38 3.4 26Z', '#fff3b8')}
  ${path('M0 -36C17 -22 17 6 12 26H-12C-17 6 -17 -22 0 -36Z', body)}
  ${path('M0 -36C8 -29 13 -23 15 -14H-15C-13 -23 -8 -29 0 -36Z', acc)}
  ${circ(0, -3, 8, M.navy)}${circ(0, -3, 4.6, M.bluL)}`;
const robotG = () => `${rect(-1.8, -31, 3.6, 11, 0, M.gray)}${circ(0, -33, 4.6, M.ter)}
  ${rect(-22, -20, 44, 31, 11, M.bluL)}${circ(-8.5, -5, 4.6, M.navy)}${circ(8.5, -5, 4.6, M.navy)}
  ${rect(-24.5, -12, 5, 12, 2.5, M.blu)}${rect(19.5, -12, 5, 12, 2.5, M.blu)}
  ${rect(-16, 14, 32, 19, 7, M.blu)}${circ(0, 23.5, 4, M.mus)}`;
const hatG = () => `${path('M-26 8A26 26 0 0 1 26 8Z', '#e8b130')}${rect(-32, 6, 64, 9, 4.5, '#d09a1c')}${rect(-5, -20, 10, 26, 4, '#f1c552')}`;
const treeG = () => `${rect(-3.5, 4, 7, 27, 3.5, M.terD)}${circ(0, -8, 23, M.grn)}${circ(-10, -2, 14, M.grnD, 'opacity=".55"')}${circ(10, -15, 9, M.grnL, 'opacity=".85"')}`;
const saplingG = pot => `${rect(-1.8, -16, 3.6, 22, 1.8, M.grn)}
  ${path('M0 -6C-20 -6 -28 -20 -26 -30C-10 -30 0 -20 0 -6Z', M.grn)}${path('M0 -12C18 -12 26 -26 24 -36C8 -36 0 -26 0 -12Z', M.grnL)}
  ${path('M-16 6H16L11 30H-11Z', pot)}${rect(-18.5, 2, 37, 7, 3.5, M.terD)}`;
const moonG = c => path('M8 -25A26 26 0 1 0 25 13A20 20 0 0 1 8 -25Z', c);
const planetG = (c, ring) => `<g transform="rotate(-18)"><path fill-rule="evenodd" fill="${ring}" d="M-34 0a34 11 0 1 0 68 0a34 11 0 1 0 -68 0ZM-29 0a29 6 0 1 1 58 0a29 6 0 1 1 -58 0Z"/>${circ(0, 0, 17, c)}<path fill="${ring}" d="M-34 0A34 11 0 0 0 34 0L29 0A29 6 0 0 1 -29 0Z"/></g>`;
const binG = (c, cD, glyph) => `${rect(-6, -33, 12, 7, 3.5, cD)}${path('M-15 -14H15L12 28Q12 31 9 31H-9Q-12 31 -12 28Z', c)}${rect(-19, -26, 38, 11, 5.5, cD)}${glyph}`;

/* ---------- 1 · Sức khỏe & dinh dưỡng ---------- */
function scene1() {
  const cx = 124, cy = 106;
  return `${blob(M.roseL, .45)}
  ${circ(cx, cy, 86, M.white)}${circ(cx, cy, 73, '#f1e8d3')}
  ${sector(cx, cy, 65, 180, 360, '#6aa56e', 3.5)}${sector(cx, cy, 65, 90, 180, '#efd7a1', 3.5)}${sector(cx, cy, 65, 0, 90, '#e4a58a', 3.5)}
  ${T(92, 78, 1, 0, `${rect(-3, 4, 6, 12, 3, '#86b97b')}${circ(-8, 0, 9, '#2f6e44')}${circ(8, 0, 9, '#2f6e44')}${circ(0, -8, 10, '#3b8250')}`)}
  ${circ(142, 76, 12, '#d9503f')}${path('M136 67Q142 61 148 67Q142 70 136 67Z', '#2f6e44')}
  ${[[112, 96], [128, 94], [150, 98]].map(([x, y]) => circ(x, y, 6.5, '#f08a3c') + circ(x, y, 3, '#f6b06c')).join('')}
  ${ell(92, 140, 25, 15, M.white)}${[[82, 137], [92, 133], [102, 138], [88, 144], [98, 145]].map(([x, y]) => ell(x, y, 3, 1.6, '#e3cf9d', 20)).join('')}
  ${ell(152, 138, 24, 18, M.white)}${circ(152, 138, 8, '#f2b632')}
  <!-- cốc nước -->
  ${path('M236 70H282L277 146Q276.5 152 271 152H247Q241.5 152 241 146Z', '#e3eef2')}
  ${path('M238.4 98H279.6L277 146Q276.5 152 271 152H247Q241.5 152 241 146Z', '#79b3d4')}
  ${circ(252, 124, 3.2, '#cfe6f2')}${circ(266, 136, 2.4, '#cfe6f2')}${circ(259, 111, 2, '#cfe6f2')}
  ${T(259, 46, .55, 0, dropG('#79b3d4'))}
  <!-- xà phòng + bọt -->
  ${rect(306, 116, 76, 40, 16, '#f0a9b2')}${rect(314, 122, 60, 10, 5, '#f8cfd3')}
  ${[[326, 84, 17], [360, 66, 10], [380, 92, 7], [338, 56, 6]].map(([x, y, r]) => circ(x, y, r, '#b9dcec') + circ(x, y, r * .68, '#dff0f7')).join('')}
  <!-- mũi tiêm vắc-xin -->
  ${T(452, 112, 1, -38, `${rect(-44, -9, 70, 18, 5, '#f4efe3')}${rect(-44, -9, 40, 18, 5, '#8cc0dc')}
    ${[-30, -20, -10, 0, 10].map(x => rect(x, -9, 2, 7, 1, '#b7bdbf')).join('')}
    ${rect(-62, -3, 20, 6, 3, '#c9cfd2')}${rect(-68, -11, 6, 22, 3, '#9aa5ab')}${rect(-48, -13, 5, 26, 2, '#9aa5ab')}
    ${rect(24, -5, 7, 10, 2, '#7fa7c0')}${path('M30 -2L62 -0.8L62 0.8L30 2Z', '#aab4b9')}`)}
  <!-- mặt trăng: ngủ đủ giấc -->
  ${T(486, 40, .8, 0, moonG(M.musL))}${T(458, 26, .6, 0, sparkG(M.mus))}${T(504, 76, .5, 0, sparkG(M.mus))}`;
}

/* ---------- 2 · Năng lượng & điện ---------- */
function scene2() {
  const rays = [0, 45, 90, 135, 180, 225, 270, 315].map(a => `<rect x="-3" y="-37" width="6" height="12" rx="3" fill="#f0c25e" transform="rotate(${a})"/>`).join('');
  const blades = [0, 120, 240].map(a => `<g transform="rotate(${a})">${ell(0, -26, 5.5, 26, '#fbfcfd')}${path('M0 -52C5 -44 6 -30 0 -4Z', '#d3e0e8')}</g>`).join('');
  return `${blob(M.musL, .4)}
  ${T(58, 50, 1, 0, rays + circ(0, 0, 22, '#e8a93c'))}
  ${T(66, 142, 1.15, 0, bulbG(true))}
  <!-- ngôi nhà có tấm pin mặt trời -->
  ${rect(186, 62, 16, 30, 2, M.terD)}
  ${rect(168, 104, 126, 72, 4, '#f7ecd4')}
  ${path('M154 110L231 50L308 110Z', M.ter)}${path('M154 110H308L300 119H162Z', M.terD)}
  ${T(268, 84, 1, 37.6, `${rect(-25, -15, 50, 30, 3, '#2f5d85')}${[0, 1, 2].flatMap(i => [0, 1].map(j => rect(-22 + i * 15.5, -12 + j * 14, 13.5, 11.5, 1.5, '#5a93bf'))).join('')}`)}
  ${rect(176, 120, 28, 28, 3, '#fbe39a')}${rect(258, 120, 28, 28, 3, '#fbe39a')}${rect(221, 136, 22, 40, 3, M.wood)}${circ(238, 158, 1.8, M.woodD)}
  <!-- tua-bin gió -->
  ${path('M368 178L376 178L374.4 104L369.6 104Z', '#d3e0e8')}${T(372, 98, 1, 0, blades + circ(0, 0, 6, M.ter))}
  <!-- ổ cắm + giọt nước cấm -->
  ${rect(420, 108, 64, 64, 14, M.white)}${circ(444, 138, 5, M.gray)}${circ(462, 138, 5, M.gray)}
  ${path('M456 118L446 134H453L450 148L462 130H455Z', M.mus)}
  ${T(470, 62, .9, 0, `${dropG('#79b3d4')}<path fill-rule="evenodd" fill="${M.rose}" d="M-30 0a30 30 0 1 0 60 0a30 30 0 1 0 -60 0ZM-24 0a24 24 0 1 1 48 0a24 24 0 1 1 -48 0Z"/>${rect(-26, -3.5, 52, 7, 3, M.rose, 'transform="rotate(-45)"')}`)}
  ${T(110, 28, .6, 0, sparkG('#fff8e6'))}`;
}

/* ---------- 3 · Hóa học quanh ta ---------- */
function scene3() {
  const tube = (x, liq, lvl) => `${path(`M${x - 11} 52H${x + 11}V132A11 11 0 0 1 ${x - 11} 132Z`, '#e8f1f4')}${path(`M${x - 11} ${lvl}H${x + 11}V132A11 11 0 0 1 ${x - 11} 132Z`, liq)}${rect(x - 14, 48, 28, 7, 3.5, '#cdd9de')}`;
  const lemonSeg = [0, 45, 90, 135, 180, 225, 270, 315].map(a => `<path d="M0 -3L-5 -24A25 25 0 0 1 5 -24Z" fill="#f6dd7a" transform="rotate(${a})"/>`).join('');
  return `${blob(M.plumL, .38)}
  <!-- chanh -->
  ${T(58, 112, 1.1, 0, circ(0, 0, 33, '#e8c43c') + circ(0, 0, 28, '#fbf0b8') + lemonSeg + circ(0, 0, 3.4, '#fbf0b8'))}
  ${T(102, 150, .9, -20, ell(0, 0, 26, 18, '#ecc83e') + path('M24 -6Q32 -10 34 -4Q30 0 24 -2Z', '#e8c43c') + path('M-4 -17Q4 -26 14 -23Q8 -14 -4 -17Z', M.grn))}
  <!-- chai giấm -->
  ${rect(148, 56, 42, 96, 12, '#9a5b34')}${rect(160, 38, 18, 22, 4, '#b57445')}${rect(158, 30, 22, 10, 4, '#3f4a55')}${rect(152, 86, 34, 38, 5, M.cream)}${rect(158, 94, 22, 5, 2.5, M.rose)}${rect(158, 104, 22, 4, 2, '#d8cdb4')}
  <!-- hộp baking soda + bọt khí CO2 -->
  ${rect(214, 86, 62, 70, 6, '#4f87bd')}${rect(214, 86, 62, 16, 4, '#3b6fa0')}${rect(224, 112, 42, 26, 4, M.white)}${circ(245, 125, 7, '#f1d08a')}
  ${[[226, 66, 6], [244, 52, 4], [260, 68, 7], [240, 72, 3], [266, 48, 3]].map(([x, y, r]) => circ(x, y, r, '#fff', 'opacity=".8"')).join('')}
  <!-- giá ống nghiệm: bắp cải tím đổi màu -->
  ${tube(336, '#e0577d', 78)}${tube(382, '#8a5cb0', 78)}${tube(428, '#3aa79c', 78)}
  ${rect(310, 138, 144, 14, 5, M.wood)}${rect(310, 146, 144, 6, 3, M.woodD)}
  <!-- lá bắp cải tím -->
  ${T(474, 118, 1, 12, path('M0 -44C28 -44 40 -16 34 14C30 36 10 46 0 46C-10 46 -30 36 -34 14C-40 -16 -28 -44 0 -44Z', '#7e4f9c') + path('M0 -40C-12 -26 -14 -2 0 40C14 -2 12 -26 0 -40Z', '#a77cc2') + path('M-24 -6C-14 0 -8 10 -3 22M24 -6C14 0 8 10 3 22', 'none', 'stroke="#a77cc2" stroke-width="4" stroke-linecap="round"'))}
  ${T(300, 36, .6, 0, sparkG('#fff'))}`;
}

/* ---------- 4 · Môi trường xanh ---------- */
function scene4() {
  const wheel = x => `<path fill-rule="evenodd" fill="${M.gray}" d="M${x - 27} 160a27 27 0 1 0 54 0a27 27 0 1 0 -54 0ZM${x - 22} 160a22 22 0 1 1 44 0a22 22 0 1 1 -44 0Z"/>`;
  return `${blob(M.grnL, .4)}
  ${inBlob(path('M0 174Q130 154 260 170T520 160V210H0Z', '#a8d1a1'))}
  <!-- túi vải + bình nước -->
  ${path('M38 84Q38 50 62 50Q86 50 86 84', 'none', `stroke="${M.woodD}" stroke-width="7" stroke-linecap="round"`)}
  ${rect(26, 80, 72, 82, 8, '#efdfb8')}${T(62, 122, .9, 0, leafG(M.grn, M.grnD))}
  ${rect(112, 96, 26, 66, 10, '#6aa0c4')}${rect(118, 82, 14, 18, 4, '#3f6a8c')}${rect(112, 118, 26, 8, 0, M.white, 'opacity=".55"')}
  <!-- 3 thùng rác + rác tương ứng -->
  ${T(196, 128, 1.15, 0, binG(M.grn, M.grnD, T(0, 8, .58, 0, leafG('#fff', '#dcebd5'))))}
  ${T(256, 128, 1.15, 0, binG(M.blu, M.bluD, T(0, 8, .5, 0, dropG('#fff'))))}
  ${T(316, 128, 1.15, 0, binG(M.gray, '#434f56', circ(0, 8, 5.5, '#fff')))}
  ${T(196, 62, 1, 0, path('M-12 -6C-18 6 -10 20 0 18C10 20 18 6 12 -6C6 -12 -6 -12 -12 -6Z', '#d9503f') + path('M-9 -2C-12 6 -8 14 0 12C8 14 12 6 9 -2C4 4 -4 4 -9 -2Z', '#f6ecd8') + circ(0, 2, 2, '#6b4a2a') + path('M0 -8Q2 -16 8 -18', 'none', `stroke="${M.terD}" stroke-width="3" stroke-linecap="round"`))}
  ${T(256, 60, 1, 14, rect(-10, -14, 20, 38, 8, '#9fd0e6') + rect(-6, -22, 12, 10, 3, '#4f87bd') + rect(-10, -2, 20, 8, 0, '#fff', 'opacity=".55"'))}
  ${T(316, 62, 1, -10, path('M-14 -16L14 -16L12 18L-12 18Z', M.mus) + path('M-14 -16L14 -16L13 -8L-13 -8Z', M.musD) + rect(-8, 0, 16, 8, 2, M.musL))}
  <!-- cây + xe đạp -->
  ${T(392, 116, 1.1, 0, treeG())}
  ${wheel(432)}${wheel(486)}
  ${path('M432 160L454 118L480 160M454 118H472', 'none', `stroke="${M.terD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`)}
  ${path('M486 160L476 112M468 112H484', 'none', `stroke="${M.gray}" stroke-width="5" stroke-linecap="round"`)}${rect(442, 106, 24, 8, 4, M.gray)}`;
}

/* ---------- 5 · Công nghệ & kĩ thuật ---------- */
function scene5() {
  const waves = (y, c) => path(`M196 ${y}Q214 ${y - 10} 232 ${y}T268 ${y}T304 ${y}T340 ${y}V200H196Z`, c);
  const pondId = 'pd' + (++_g);
  return `${blob(M.bluL, .42)}
  <!-- cái kéo (đòn bẩy) -->
  ${T(72, 52, 1, -32, `${path('M-4 2L40 -8L40 -4L-2 8Z', '#c4ccd1')}${path('M-4 -2L40 8L40 4L-2 -8Z', '#aeb8be')}<path fill-rule="evenodd" fill="${M.ter}" d="M-30 12a12 12 0 1 0 24 0a12 12 0 1 0 -24 0ZM-26 12a8 8 0 1 1 16 0a8 8 0 1 1 -16 0Z"/><path fill-rule="evenodd" fill="${M.terD}" d="M-30 -12a12 12 0 1 0 24 0a12 12 0 1 0 -24 0ZM-26 -12a8 8 0 1 1 16 0a8 8 0 1 1 -16 0Z"/>${circ(0, 0, 3.4, M.gray)}`)}
  <!-- bập bênh -->
  ${path('M72 176H112L92 134Z', M.terD)}
  ${T(92, 136, 1, -12, rect(-66, -5, 132, 10, 5, M.mus) + rect(-62, -34, 30, 29, 4, M.wood) + rect(-62, -22, 30, 4, 0, M.woodD) + circ(52, -14, 9, M.rose))}
  <!-- ao nước có thuyền nổi (lực đẩy Archimedes) -->
  <clipPath id="${pondId}"><rect x="196" y="96" width="144" height="86" rx="26"/></clipPath>
  <g clip-path="url(#${pondId})">${rect(196, 96, 144, 86, 0, '#d4e6f1')}${waves(132, '#8fbbd6')}${waves(152, M.blu)}</g>
  ${T(268, 112, 1.25, 0, path('M-24 0H24L15 20H-15Z', M.ter) + path('M-2 -4V-46L22 -4Z', M.cream) + path('M-2 -4V-34L-18 -4Z', '#e9dfc8') + rect(-3, -48, 3, 52, 1, M.gray))}
  ${waves(144, 'none')}
  <!-- bình giữ nhiệt + cốc -->
  ${rect(384, 40, 44, 22, 8, M.ter)}${rect(378, 58, 56, 108, 16, '#4b86ae')}${rect(378, 100, 56, 12, 0, M.cream, 'opacity=".9"')}${rect(388, 70, 8, 86, 4, '#fff', 'opacity=".25"')}
  ${circ(396, 28, 4, '#fff', 'opacity=".7"')}${circ(410, 18, 3, '#fff', 'opacity=".7"')}${circ(402, 8, 2.4, '#fff', 'opacity=".7"')}
  ${rect(448, 128, 44, 38, 10, M.cream)}${path('M492 138Q510 138 510 150Q510 162 492 162', 'none', `stroke="${M.cream}" stroke-width="7"`)}${rect(450, 130, 40, 10, 5, '#8a5a3c')}
  ${T(470, 96, .5, 0, sparkG('#fff'))}`;
}

/* ---------- 6 · Kết nối tương lai ---------- */
function scene6() {
  const badge = (x, y, ic) => circ(x, y, 32, M.white) + T(x, y + 2, .72, 0, ic);
  return `${blob(M.terL, .4)}
  ${[[150, 30], [372, 36], [336, 100], [186, 104], [410, 150], [118, 160]].map(([x, y], i) => circ(x, y, i % 2 ? 2.6 : 3.4, M.white, 'opacity=".9"')).join('')}
  ${T(140, 52, 1, 0, planetG(M.mus, M.terL))}${T(380, 66, .7, 0, moonG(M.cream))}
  <!-- cuốn sách mở, tên lửa bay ra -->
  ${circ(222, 142, 15, M.white, 'opacity=".95"')}${circ(254, 150, 19, M.white, 'opacity=".95"')}${circ(290, 142, 15, M.white, 'opacity=".95"')}
  ${T(256, 78, 1.55, 0, rocketG())}
  ${path('M260 168C232 152 196 150 160 156L160 184C198 178 234 180 260 194Z', '#fffdf7')}${path('M260 168C288 152 324 150 360 156L360 184C322 178 286 180 260 194Z', '#f1e8d3')}
  ${path('M260 168V194', 'none', `stroke="${M.terL}" stroke-width="3"`)}
  <!-- bốn nghề -->
  ${badge(54, 66, heartG(M.rose))}${badge(54, 140, hatG())}${badge(466, 66, flaskG(M.plum))}${badge(466, 140, robotG())}`;
}

/* ---------- trái tim giữa trang ---------- */
function heartCenter() {
  return `<svg viewBox="0 0 250 330" xmlns="http://www.w3.org/2000/svg" font-family="M PLUS Rounded 1c, sans-serif">
    <path d="M125 62C121 40 128 20 146 12C160 28 158 52 125 62Z" fill="${M.grn}"/>
    <path d="M125 66C108 56 96 36 78 30C76 50 92 70 125 66Z" fill="${M.grnL}"/>
    <path d="M125 84V58" stroke="${M.grn}" stroke-width="5" stroke-linecap="round"/>
    <path d="M125 238C28 172 6 112 32 78C56 50 100 60 125 96C150 60 194 50 218 78C244 112 222 172 125 238Z" fill="#e9a8ab"/>
    <g text-anchor="middle" fill="${M.ink}" font-weight="900">
      <text x="125" y="140" font-size="56" fill="${M.rose}">6</text>
      <text x="125" y="170" font-size="25">ứng dụng</text>
      <text x="125" y="198" font-size="25">của KHTN</text>
    </g>
    <path d="M125 322C70 322 28 296 20 244C70 248 112 276 125 322Z" fill="${M.grn}"/>
    <path d="M125 322C180 322 222 296 230 244C180 248 138 276 125 322Z" fill="${M.grnL}"/>
  </svg>`;
}

/* ---------- biểu tượng cho dải cam kết ---------- */
const pledgeIcons = {
  health: `<svg viewBox="-34 -34 68 68">${heartG(M.rose)}</svg>`,
  energy: `<svg viewBox="-34 -34 68 68">${path('M-9 14C-9 7 -20 3 -20 -9A20 20 0 1 1 20 -9C20 3 9 7 9 14Z', '#efb93a')}${rect(-9, 14, 18, 6, 3, M.gray)}${rect(-6.5, 21, 13, 5, 2.5, M.gray)}</svg>`,
  chem: `<svg viewBox="-34 -34 68 68">${flaskG(M.plum)}</svg>`,
  eco: `<svg viewBox="-34 -38 68 72">${saplingG(M.ter)}</svg>`,
  tech: `<svg viewBox="-34 -34 68 68">${gearG(M.blu)}</svg>`,
  future: `<svg viewBox="-34 -40 68 80">${rocketG()}</svg>`
};
