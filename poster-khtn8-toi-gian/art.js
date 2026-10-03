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
  navy: '#233a5c', gray: '#5d6b73', grayL: '#a9b3b8', wood: '#c79a63', woodD: '#a67a46',
  skin: '#e6b08a'
};
const rad = d => d * Math.PI / 180;
const T = (x, y, s = 1, rot = 0, inner = '') => `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">${inner}</g>`;
const rect = (x, y, w, h, r, f, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${f}" ${extra}/>`;
const circ = (x, y, r, f, extra = '') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${f}" ${extra}/>`;
const ell = (x, y, rx, ry, f, rot = 0) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${f}" transform="rotate(${rot} ${x} ${y})"/>`;
const path = (d, f, extra = '') => `<path d="${d}" fill="${f}" ${extra}/>`;
const bar = (d, c, w) => `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
const ring = (cx, cy, R, r, f) => `<path fill-rule="evenodd" fill="${f}" d="M${cx - R} ${cy}a${R} ${R} 0 1 0 ${2 * R} 0a${R} ${R} 0 1 0 ${-2 * R} 0ZM${cx - r} ${cy}a${r} ${r} 0 1 1 ${2 * r} 0a${r} ${r} 0 1 1 ${-2 * r} 0Z"/>`;

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
  ${path('M-9 14C-9 7 -20 3 -20 -9A20 20 0 1 1 20 -9C20 3 9 7 9 14Z', lit ? '#f7d77f' : '#e3e8eb')}
  ${rect(-9, 14, 18, 6, 3, M.gray)}${rect(-6.5, 21, 13, 5, 2.5, M.gray)}
  ${lit ? bar('M-4 12V-1L0 -6L4 -1V12', '#d99a2b', 2.2) : bar('M-4 12V-1L0 -6L4 -1V12', '#b7c0c6', 2.2)}`;
const heartG = c => path('M0 24C-32 3 -28 -20 -13 -23C-6 -24 -1 -19 0 -15C1 -19 6 -24 13 -23C28 -20 32 3 0 24Z', c);
const crossG = c => rect(-9, -26, 18, 52, 6, c) + rect(-26, -9, 52, 18, 6, c);
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
const moonG = c => path('M8 -25A26 26 0 1 0 25 13A20 20 0 0 1 8 -25Z', c);
const saplingG = pot => `${rect(-1.8, -16, 3.6, 22, 1.8, M.grn)}
  ${path('M0 -6C-20 -6 -28 -20 -26 -30C-10 -30 0 -20 0 -6Z', M.grn)}${path('M0 -12C18 -12 26 -26 24 -36C8 -36 0 -26 0 -12Z', M.grnL)}
  ${path('M-16 6H16L11 30H-11Z', pot)}${rect(-18.5, 2, 37, 7, 3.5, M.terD)}`;

const beakerG = liq => `${path('M-18 -24H18V18Q18 28 8 28H-8Q-18 28 -18 18Z', '#e7f0f3')}${path('M-18 -2H18V18Q18 28 8 28H-8Q-18 28 -18 18Z', liq)}${rect(-22, -27, 44, 6, 3, M.gray)}${[-14, -6, 2].map(y => rect(-18, y, 9, 2.4, 1, '#a9b3b8')).join('')}`;
/* cây non đang được trồng xuống đất, có xẻng */
const plantG = () => `${ell(0, 24, 30, 9, '#8b6a4a')}${rect(-1.8, -18, 3.6, 40, 1.8, M.grn)}
  ${path('M0 -4C-20 -4 -28 -18 -26 -28C-10 -28 0 -18 0 -4Z', M.grn)}${path('M0 -12C18 -12 26 -26 24 -36C8 -36 0 -26 0 -12Z', M.grnL)}
  ${rect(31, -10, 5, 38, 2.5, M.wood)}${rect(26, -12, 15, 5, 2.5, M.woodD)}${path('M26 26H41L39 42Q33.5 48 28 42Z', M.grayL)}`;

/* thùng rác có bánh xe: tách rõ với cốc nước */
const binG = (c, cD, glyph) => `${circ(-9, 32, 4.6, M.gray)}${circ(9, 32, 4.6, M.gray)}${rect(-6, -35, 12, 7, 3.5, cD)}
  ${path('M-16 -14H16L14 27Q14 30 11 30H-11Q-14 30 -14 27Z', c)}${rect(-20, -26, 40, 12, 6, cD)}${glyph}`;
const recycleG = () => {
  const r = 9.5, cy = 8, arrow = (a0, a1) => {
    const P = a => [r * Math.cos(rad(a)), cy + r * Math.sin(rad(a))];
    const [x0, y0] = P(a0), [x1, y1] = P(a1);
    const tx = -Math.sin(rad(a1)), ty = Math.cos(rad(a1)), nx = Math.cos(rad(a1)), ny = Math.sin(rad(a1));
    const tip = [x1 + tx * 7, y1 + ty * 7], b1 = [x1 + nx * 5.2 - tx, y1 + ny * 5.2 - ty], b2 = [x1 - nx * 5.2 - tx, y1 - ny * 5.2 - ty];
    return `<path d="M${x0.toFixed(1)} ${y0.toFixed(1)}A${r} ${r} 0 0 1 ${x1.toFixed(1)} ${y1.toFixed(1)}" fill="none" stroke="#fff" stroke-width="3.6"/>` +
      `<path d="M${tip[0].toFixed(1)} ${tip[1].toFixed(1)}L${b1[0].toFixed(1)} ${b1[1].toFixed(1)}L${b2[0].toFixed(1)} ${b2[1].toFixed(1)}Z" fill="#fff"/>`;
  };
  return arrow(-80, 70) + arrow(100, 250);
};
const chipBagG = () => path('M-7 -2L-4.5 1L-2 -2L0.5 1L3 -2L5.5 1L7 -2V17L4.5 20L2 17L-0.5 20L-3 17L-5.5 20L-7 17Z', '#fff', 'transform="translate(0 4)"');

/* cái kéo: hai tay đòn bắt chéo ở chốt, tay cầm gắn liền lưỡi */
const scissorsG = () => `
  ${path('M58 17L2 9L6 -6Z', '#8c9aa4')}${bar('M4 0L-22 -19', M.terD, 7)}${ring(-30, -26, 13, 8, M.terD)}
  ${path('M58 -17L2 -9L6 6Z', '#a9b6be')}${bar('M4 0L-22 19', M.ter, 7)}${ring(-30, 26, 13, 8, M.ter)}
  ${circ(3, 0, 4.8, M.gray)}`;

/* bàn tay ướt + giọt nước */
const handG = () => `${rect(-16, -4, 32, 30, 12, M.skin)}
  ${[0, 1, 2, 3].map(i => rect(-15 + i * 9.8, -28 - (i === 1 || i === 2 ? 7 : 0) + (i === 0 ? 5 : 0), 8, 36, 4, M.skin)).join('')}
  ${T(-20, 8, 1, -36, rect(-4.5, -4, 9, 25, 4.5, M.skin))}
  ${[[-10, 40], [4, 48], [16, 38]].map(([x, y]) => T(x, y, .26, 0, dropG('#79b3d4'))).join('')}`;
const socketG = () => `${rect(-29, -29, 58, 58, 14, M.white)}${circ(-11, 0, 5, M.gray)}${circ(11, 0, 5, M.gray)}${rect(-3.5, -23, 7, 7, 2, M.grayL)}${rect(-3.5, 16, 7, 7, 2, M.grayL)}`;
const switchG = () => `${rect(0, 0, 46, 66, 11, M.white)}${rect(11, 10, 24, 46, 7, '#e3e7ea')}${rect(13, 32, 20, 22, 6, '#9aa5ab')}`;

/* bắp cải tím: cả búp tròn nhiều lớp lá */
const cabbageG = () => `${path('M-34 14C-38 -10 -22 -32 0 -34C22 -32 38 -10 34 14C28 30 -28 30 -34 14Z', '#6b3f8a')}
  ${circ(0, 0, 29, '#7e4f9c')}
  ${path('M-24 -12C-8 -28 16 -28 26 -8C10 -16 -10 -16 -24 -12Z', '#9468b4')}
  ${path('M-28 6C-14 -6 12 -6 28 8C14 2 -12 2 -28 6Z', '#9468b4')}
  ${path('M-22 20C-8 10 12 10 24 20C10 16 -10 16 -22 20Z', '#9468b4')}
  ${bar('M-3 -29C-9 -10 -9 10 -3 29', '#b896cf', 3)}`;

const laptopG = () => `${rect(-34, -24, 68, 44, 5, M.navy)}${rect(-26, -14, 30, 4, 2, '#7fd1a8')}${rect(-26, -5, 44, 4, 2, M.musL)}${rect(-26, 4, 24, 4, 2, M.bluL)}
  ${path('M-42 24H42L36 31H-36Z', M.grayL)}`;
const magnifierG = () => `${circ(0, 0, 18, '#fbe4dc')}${ring(0, 0, 25, 18, M.ter)}<g transform="rotate(45)">${rect(24, -5, 34, 10, 5, M.terD)}</g>`;
const planetG = (c, rg) => `<g transform="rotate(-18)"><path fill-rule="evenodd" fill="${rg}" d="M-34 0a34 11 0 1 0 68 0a34 11 0 1 0 -68 0ZM-29 0a29 6 0 1 1 58 0a29 6 0 1 1 -58 0Z"/>${circ(0, 0, 17, c)}<path fill="${rg}" d="M-34 0A34 11 0 0 0 34 0L29 0A29 6 0 0 1 -29 0Z"/></g>`;

/* tàu hàng thép nổi trên mặt nước */
const shipG = () => `${path('M-46 0H46L36 22H-36Z', '#3f566e')}${rect(-42, 3, 84, 5, 0, M.ter)}
  ${rect(-4, -22, 34, 22, 3, M.white)}${rect(10, -34, 11, 14, 2, M.ter)}
  ${rect(-40, -14, 15, 14, 2, M.mus)}${rect(-24, -14, 15, 14, 2, M.blu)}${rect(-40, -28, 15, 13, 2, M.rose)}`;

/* xe đạp có bàn đạp, líp và xích */
const bikeG = () => `${ring(-30, 0, 24, 19.5, M.gray)}${ring(30, 0, 24, 19.5, M.gray)}${circ(-30, 0, 3.4, M.gray)}${circ(30, 0, 3.4, M.gray)}
  ${bar('M-30 0L-6 4L-14 -28L16 -30L-6 4M16 -30L30 0M16 -30L19 -39', M.terD, 4.6)}
  ${bar('M-14 -28L-17 -37', M.gray, 3.4)}${rect(-26, -44, 20, 7, 3.5, M.gray)}${bar('M19 -39L27 -42', M.gray, 4)}
  ${circ(-6, 4, 8.5, M.grayL)}${bar('M-6 4L3 15', M.gray, 3.6)}${rect(-1, 14, 11, 4.4, 2.2, M.gray)}
  ${bar('M-30 -3L-6 -4M-30 3L-6 12', M.gray, 1.8)}`;

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
  ${rect(306, 116, 76, 40, 16, '#f0a9b2')}
  ${[[326, 84, 17], [360, 66, 10], [380, 92, 7], [338, 56, 6]].map(([x, y, r]) => circ(x, y, r, '#b9dcec') + circ(x, y, r * .68, '#dff0f7')).join('')}
  <!-- mũi tiêm vắc-xin -->
  ${T(452, 112, 1, -38, `${rect(-44, -9, 70, 18, 5, '#f4efe3')}${rect(-44, -9, 40, 18, 5, '#8cc0dc')}
    ${[-30, -20, -10, 0, 10].map(x => rect(x, -9, 2, 7, 1, '#b7bdbf')).join('')}
    ${rect(-62, -3, 20, 6, 3, '#c9cfd2')}${rect(-68, -11, 6, 22, 3, '#9aa5ab')}${rect(-48, -13, 5, 26, 2, '#9aa5ab')}
    ${rect(24, -5, 7, 10, 2, '#7fa7c0')}${path('M30 -2L62 -0.8L62 0.8L30 2Z', '#aab4b9')}`)}
  <!-- mặt trăng: ngủ đủ giấc -->
  ${T(466, 58, .72, 0, moonG(M.musL))}${T(440, 36, .5, 0, sparkG(M.mus))}`;
}

/* ---------- 2 · Năng lượng & điện ---------- */
function scene2() {
  const rays = [0, 45, 90, 135, 180, 225, 270, 315].map(a => `<rect x="-3" y="-35" width="6" height="11" rx="3" fill="#f0c25e" transform="rotate(${a})"/>`).join('');
  const blades = [0, 120, 240].map(a => `<g transform="rotate(${a})">${ell(0, -26, 5.5, 26, '#fbfcfd')}${path('M0 -52C5 -44 6 -30 0 -4Z', '#d3e0e8')}</g>`).join('');
  return `${blob(M.musL, .4)}
  ${T(52, 40, .95, 0, rays + circ(0, 0, 21, '#e8a93c'))}
  <!-- công tắc đang ở vị trí TẮT + bóng đèn tắt -->
  ${T(26, 86, 1, 0, switchG())}${T(106, 130, 1.05, 0, bulbG(false))}
  <!-- ngôi nhà có tấm pin mặt trời -->
  ${rect(196, 62, 16, 30, 2, M.terD)}
  ${rect(178, 104, 126, 72, 4, '#f7ecd4')}
  ${path('M164 110L241 50L318 110Z', M.ter)}${path('M164 110H318L310 119H172Z', M.terD)}
  ${T(278, 84, 1, 37.6, `${rect(-25, -15, 50, 30, 3, '#2f5d85')}${[0, 1, 2].flatMap(i => [0, 1].map(j => rect(-22 + i * 15.5, -12 + j * 14, 13.5, 11.5, 1.5, '#5a93bf'))).join('')}`)}
  ${rect(186, 120, 28, 28, 3, '#fbe39a')}${rect(268, 120, 28, 28, 3, '#fbe39a')}${rect(231, 136, 22, 40, 3, M.wood)}${circ(248, 158, 1.8, M.woodD)}
  <!-- tua-bin gió -->
  ${path('M368 178L376 178L374.4 104L369.6 104Z', '#d3e0e8')}${T(372, 98, 1, 0, blades + circ(0, 0, 6, M.ter))}
  <!-- tay ướt + ổ cắm: cấm -->
  ${T(462, 78, .86, 0, `${handG()}<path fill-rule="evenodd" fill="${M.rose}" d="M-46 6a46 46 0 1 0 92 0a46 46 0 1 0 -92 0ZM-40 6a40 40 0 1 1 80 0a40 40 0 1 1 -80 0Z"/>${rect(-42, 2.5, 84, 7, 3, M.rose, 'transform="rotate(-45 0 6)"')}`)}
  ${T(462, 156, .78, 0, socketG())}
  ${T(112, 28, .6, 0, sparkG('#fff8e6'))}`;
}

/* ---------- 3 · Hóa học quanh ta ---------- */
function scene3() {
  const tube = (x, liq, lvl) => `${path(`M${x - 11} 52H${x + 11}V132A11 11 0 0 1 ${x - 11} 132Z`, '#e8f1f4')}${path(`M${x - 11} ${lvl}H${x + 11}V132A11 11 0 0 1 ${x - 11} 132Z`, liq)}${rect(x - 14, 48, 28, 7, 3.5, '#cdd9de')}`;
  const lemonSeg = [0, 45, 90, 135, 180, 225, 270, 315].map(a => `<path d="M0 -3L-5 -24A25 25 0 0 1 5 -24Z" fill="#f6dd7a" transform="rotate(${a})"/>`).join('');
  return `${blob(M.plumL, .38)}
  <!-- chanh -->
  ${T(58, 112, 1.1, 0, circ(0, 0, 33, '#e8c43c') + circ(0, 0, 28, '#fbf0b8') + lemonSeg + circ(0, 0, 3.4, '#fbf0b8'))}
  ${T(102, 150, .9, -20, ell(0, 0, 26, 18, '#ecc83e') + path('M24 -6Q32 -10 34 -4Q30 0 24 -2Z', '#e8c43c') + path('M-4 -17Q4 -26 14 -23Q8 -14 -4 -17Z', M.grn))}
  <!-- chai giấm có nhãn -->
  ${rect(148, 56, 42, 96, 12, '#9a5b34')}${rect(160, 38, 18, 22, 4, '#b57445')}${rect(158, 30, 22, 10, 4, '#3f4a55')}${rect(152, 84, 34, 44, 5, M.cream)}
  <text x="169" y="111" text-anchor="middle" font-size="12.5" font-weight="900" fill="${M.rose}">GIẤM</text>
  <!-- hộp baking soda + bọt khí CO2 -->
  ${rect(214, 86, 62, 70, 6, '#4f87bd')}${rect(214, 86, 62, 16, 4, '#3b6fa0')}${rect(222, 110, 46, 30, 4, M.white)}
  <text x="245" y="130" text-anchor="middle" font-size="12" font-weight="900" fill="#3b6fa0">SODA</text>
  ${[[226, 66, 6], [244, 52, 4], [260, 68, 7], [240, 72, 3], [266, 48, 3]].map(([x, y, r]) => circ(x, y, r, '#fff', 'opacity=".8"')).join('')}
  <!-- giá ống nghiệm: bắp cải tím đổi màu -->
  ${tube(324, '#e0577d', 78)}${tube(368, '#8a5cb0', 78)}${tube(412, '#3aa79c', 78)}
  ${rect(298, 138, 138, 14, 5, M.wood)}${rect(298, 146, 138, 6, 3, M.woodD)}
  <!-- búp bắp cải tím -->
  ${T(472, 112, .86, 8, cabbageG())}
  ${T(296, 36, .6, 0, sparkG('#fff'))}`;
}

/* ---------- 4 · Môi trường xanh ---------- */
function scene4() {
  return `${blob(M.grnL, .4)}
  ${inBlob(path('M0 174Q130 154 260 170T520 160V210H0Z', '#a8d1a1'))}
  <!-- túi vải + bình nước -->
  ${bar('M38 84Q38 50 62 50Q86 50 86 84', M.woodD, 7)}
  ${rect(26, 80, 72, 82, 8, '#efdfb8')}${T(62, 122, .9, 0, leafG(M.grn, M.grnD))}
  ${rect(112, 96, 26, 66, 10, '#6aa0c4')}${rect(118, 82, 14, 18, 4, '#3f6a8c')}${rect(112, 118, 26, 8, 0, '#cfe3ef')}
  <!-- 3 thùng rác có bánh xe + rác tương ứng -->
  ${T(190, 126, 1.15, 0, binG(M.grn, M.grnD, T(0, 8, .58, 0, leafG('#fff', '#dcebd5'))))}
  ${T(248, 126, 1.15, 0, binG(M.blu, M.bluD, recycleG()))}
  ${T(306, 126, 1.15, 0, binG(M.gray, '#434f56', chipBagG()))}
  ${T(190, 60, 1, 0, path('M-12 -6C-18 6 -10 20 0 18C10 20 18 6 12 -6C6 -12 -6 -12 -12 -6Z', '#d9503f') + path('M-9 -2C-12 6 -8 14 0 12C8 14 12 6 9 -2C4 4 -4 4 -9 -2Z', '#f6ecd8') + circ(0, 2, 2, '#6b4a2a') + bar('M0 -8Q2 -16 8 -18', M.terD, 3))}
  ${T(248, 58, 1, 14, rect(-10, -14, 20, 38, 8, '#9fd0e6') + rect(-6, -22, 12, 10, 3, '#4f87bd') + rect(-10, -2, 20, 8, 0, '#d7ecf5'))}
  ${T(306, 60, 1, -10, path('M-14 -16L14 -16L12 18L-12 18Z', M.mus) + path('M-14 -16L14 -16L13 -8L-13 -8Z', M.musD) + rect(-8, 0, 16, 8, 2, M.musL))}
  <!-- trồng thêm cây + xe đạp -->
  ${T(354, 128, 1.05, 0, plantG())}
  ${T(446, 146, .85, 0, bikeG())}`;
}

/* ---------- 5 · Công nghệ & kĩ thuật ---------- */
function scene5() {
  const waves = (y, c, o = 1) => path(`M196 ${y}Q214 ${y - 10} 232 ${y}T268 ${y}T304 ${y}T340 ${y}V200H196Z`, c, `opacity="${o}"`);
  const pondId = 'pd' + (++_g);
  return `${blob(M.bluL, .42)}
  <!-- cái kéo (đòn bẩy) -->
  ${T(86, 58, .82, -16, scissorsG())}
  <!-- bập bênh -->
  ${path('M72 176H112L92 134Z', M.terD)}
  ${T(92, 136, 1, -12, rect(-66, -5, 132, 10, 5, M.mus) + rect(-62, -34, 30, 29, 4, M.wood) + rect(-62, -22, 30, 4, 0, M.woodD) + circ(52, -14, 9, M.rose))}
  <!-- tàu thép nổi trên mặt nước (lực đẩy Archimedes) -->
  <clipPath id="${pondId}"><rect x="196" y="98" width="144" height="84" rx="26"/></clipPath>
  <g clip-path="url(#${pondId})">${rect(196, 98, 144, 84, 0, '#d4e6f1')}${waves(130, '#8fbbd6')}</g>
  ${T(268, 112, .95, 0, shipG())}
  <g clip-path="url(#${pondId})">${waves(128, M.blu, .93)}${waves(150, M.bluD, .95)}</g>
  <!-- bình giữ nhiệt + cốc nóng -->
  ${rect(384, 40, 44, 22, 8, M.ter)}${rect(378, 58, 56, 108, 16, '#4b86ae')}${rect(378, 100, 56, 12, 0, M.cream)}
  ${circ(396, 28, 4, '#fff', 'opacity=".7"')}${circ(410, 18, 3, '#fff', 'opacity=".7"')}${circ(402, 8, 2.4, '#fff', 'opacity=".7"')}
  ${rect(448, 130, 44, 36, 10, M.cream)}${bar('M492 140Q508 140 508 151Q508 162 492 162', M.cream, 7)}${rect(450, 132, 40, 10, 5, '#8a5a3c')}
  ${bar('M462 122Q458 114 464 108Q470 102 466 94M476 122Q472 114 478 108Q484 102 480 94', '#ffffff', 3)}
  ${T(470, 84, .5, 0, sparkG('#fff'))}`;
}

/* ---------- 6 · Kết nối tương lai ---------- */
function scene6() {
  const badge = (x, y, ic) => circ(x, y, 31, M.white) + T(x, y + 1, .7, 0, ic);
  return `${blob(M.terL, .4)}
  ${[[150, 24], [372, 30], [196, 96], [330, 100], [420, 108], [112, 100]].map(([x, y], i) => circ(x, y, i % 2 ? 2.4 : 3.2, M.white, 'opacity=".9"')).join('')}
  <!-- quan sát + đặt câu hỏi -->
  ${T(58, 50, .95, 0, magnifierG())}
  ${circ(124, 32, 17, M.white)}<text x="124" y="41" text-anchor="middle" font-size="26" font-weight="900" fill="${M.ter}">?</text>
  <!-- thí nghiệm + công nghệ -->
  ${T(378, 56, 1.1, 0, flaskG(M.plum))}${[[366, 24, 4], [382, 14, 3], [394, 28, 2.6]].map(([x, y, r]) => circ(x, y, r, '#fff', 'opacity=".85"')).join('')}
  ${T(456, 62, .8, 0, laptopG())}
  <!-- tên lửa bay ra từ trang sách -->
  ${T(260, 62, 1.42, 0, rocketG())}
  ${circ(228, 134, 14, '#fbe6dc')}${circ(260, 139, 18, '#fbe6dc')}${circ(292, 134, 14, '#fbe6dc')}
  ${path('M260 158C234 144 202 142 172 148L172 176C204 170 236 172 260 184Z', '#fffdf7')}${path('M260 158C286 144 318 142 348 148L348 176C316 170 284 172 260 184Z', '#f1e8d3')}
  <!-- bốn nghề: bác sĩ, kĩ sư, nhà hóa học, chuyên gia AI -->
  ${badge(60, 148, crossG(M.rose))}${badge(128, 148, hatG())}${badge(392, 148, beakerG('#3aa79c'))}${badge(460, 148, robotG())}`;
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
