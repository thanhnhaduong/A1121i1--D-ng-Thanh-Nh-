/* flat.js — biểu tượng phẳng, tối giản: chỉ dùng mảng màu, KHÔNG viền, KHÔNG mũi tên/nhãn kỹ thuật.
   Mỗi hàm trả về SVG vẽ quanh gốc (0,0), kích thước danh nghĩa ~ 60 x 60. */
const P = {
  ink: '#1c1a16', cream: '#f6efdb', paper: '#f2e9d0',
  terra: '#c8553d', terraD: '#a2402b', mustard: '#e2a73b', mustardL: '#f0d9a4',
  sage: '#a9c3a0', sageL: '#d3e0c9', green: '#3f6b4f', greenD: '#2d5140',
  teal: '#214e5f', tealM: '#3a7487', sky: '#a9cfd9', skyL: '#dbe9ee',
  blush: '#e8b9a5', blushL: '#f3dcd2', navy: '#1b2a45', graphite: '#5d6b73'
};
const G = (x, y, s, inner, rot = 0) => `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">${inner}</g>`;
let _uid = 0;
const uid = p => `${p}${++_uid}`;

const fLeaf = (a = P.green, b = P.greenD) => `
  <path d="M-24 24C-32 -6 -6 -30 26 -28C28 6 4 32 -24 24Z" fill="${a}"/>
  <path d="M-24 24C-8 12 12 -6 26 -28C28 6 4 32 -24 24Z" fill="${b}"/>`;

const fDrop = (a = P.teal, hl = P.sky) => `
  <path d="M0 -30C0 -30 -22 -4 -22 10A22 22 0 0 0 22 10C22 -4 0 -30 0 -30Z" fill="${a}"/>
  <ellipse cx="-9" cy="9" rx="3.6" ry="7" fill="${hl}" opacity=".7" transform="rotate(18 -9 9)"/>`;

const fHeart = (a = P.terra) => `
  <path d="M0 24C-32 3 -28 -20 -13 -23C-6 -24 -1 -19 0 -15C1 -19 6 -24 13 -23C28 -20 32 3 0 24Z" fill="${a}"/>
  <ellipse cx="-14" cy="-9" rx="3.4" ry="6" fill="#fff" opacity=".35" transform="rotate(35 -14 -9)"/>`;

const fBulb = (glow = P.mustard, body = '#f7d77f') => `
  <circle cy="-6" r="31" fill="${glow}" opacity=".28"/>
  <path d="M-9 14C-9 7 -20 3 -20 -9A20 20 0 1 1 20 -9C20 3 9 7 9 14Z" fill="${body}"/>
  <rect x="-9" y="14" width="18" height="6" rx="3" fill="${P.graphite}"/>
  <rect x="-6.5" y="21" width="13" height="5" rx="2.5" fill="${P.graphite}"/>
  <ellipse cx="-8" cy="-12" rx="3" ry="6" fill="#fff" opacity=".5" transform="rotate(25 -8 -12)"/>`;

function fGear(c = P.mustard, R = 27, r = 21, n = 8, hole = 8.5) {
  const s = (2 * Math.PI) / n;
  let d = '';
  for (let i = 0; i < n; i++) {
    const a = i * s;
    [[a - s * 0.21, r], [a - s * 0.12, R], [a + s * 0.12, R], [a + s * 0.21, r]].forEach(([ang, rad], j) => {
      d += (i === 0 && j === 0 ? 'M' : 'L') + (rad * Math.cos(ang)).toFixed(1) + ' ' + (rad * Math.sin(ang)).toFixed(1) + ' ';
    });
  }
  d += `ZM${hole} 0A${hole} ${hole} 0 1 0 ${-hole} 0A${hole} ${hole} 0 1 0 ${hole} 0Z`;
  return `<path fill-rule="evenodd" d="${d}" fill="${c}"/>`;
}

function fFlask(liq = P.teal, glass = P.skyL) {
  const id = uid('fl');
  const d = 'M-8 -28H8V-10L26 22Q30 30 22 30H-22Q-30 30 -26 22L-8 -10Z';
  return `<clipPath id="${id}"><path d="${d}"/></clipPath>
    <path d="${d}" fill="${glass}"/>
    <g clip-path="url(#${id})"><rect x="-32" y="6" width="64" height="30" fill="${liq}"/>
      <circle cx="-7" cy="17" r="3.4" fill="#fff" opacity=".55"/><circle cx="8" cy="22" r="2.4" fill="#fff" opacity=".55"/></g>
    <rect x="-11" y="-32" width="22" height="6" rx="3" fill="${P.graphite}"/>`;
}

const fAtom = (ring = P.terra, nuc = P.mustard) => {
  const R = '<path fill-rule="evenodd" d="M-30 0a30 10 0 1 0 60 0a30 10 0 1 0 -60 0ZM-25.6 0a25.6 5.6 0 1 1 51.2 0a25.6 5.6 0 1 1 -51.2 0Z"/>';
  return `<g fill="${ring}">${R}<g transform="rotate(60)">${R}</g><g transform="rotate(120)">${R}</g></g>
    <circle r="7.5" fill="${nuc}"/><circle cx="30" r="3.6" fill="${P.teal}"/>
    <g transform="rotate(60)"><circle cx="-30" r="3.6" fill="${P.teal}"/></g><g transform="rotate(120)"><circle cx="30" r="3.6" fill="${P.teal}"/></g>`;
};

const fRocket = (body = P.cream, accent = P.terra) => `
  <path d="M-11 4L-25 28L-11 24Z" fill="${accent}"/><path d="M11 4L25 28L11 24Z" fill="${accent}"/>
  <path d="M-7 26Q0 50 7 26Z" fill="${P.mustard}"/><path d="M-3.4 26Q0 38 3.4 26Z" fill="#fff3b8"/>
  <path d="M0 -36C17 -22 17 6 12 26H-12C-17 6 -17 -22 0 -36Z" fill="${body}"/>
  <path d="M0 -36C8 -29 13 -23 15 -14H-15C-13 -23 -8 -29 0 -36Z" fill="${accent}"/>
  <circle cy="-3" r="8" fill="${P.navy}"/><circle cx="-2" cy="-5" r="3" fill="${P.sky}"/>`;

const fPlanet = (c = P.mustard, ring = P.blush) => `
  <g transform="rotate(-18)"><path fill-rule="evenodd" fill="${ring}" d="M-34 0a34 11 0 1 0 68 0a34 11 0 1 0 -68 0ZM-29 0a29 6 0 1 1 58 0a29 6 0 1 1 -58 0Z"/>
  <circle r="17" fill="${c}"/>
  <path fill="${ring}" d="M-34 0A34 11 0 0 0 34 0L29 0A29 6 0 0 1 -29 0Z"/></g>`;

const fMoon = (c = P.cream) => `<path d="M8 -25A26 26 0 1 0 25 13A20 20 0 0 1 8 -25Z" fill="${c}"/>`;
const fSpark = (c = P.mustard) => `<path d="M0 -11Q1.6 -1.6 11 0Q1.6 1.6 0 11Q-1.6 1.6 -11 0Q-1.6 -1.6 0 -11Z" fill="${c}"/>`;

const fSapling = (pot = P.terra) => `
  <rect x="-1.8" y="-16" width="3.6" height="22" rx="1.8" fill="${P.green}"/>
  <path d="M0 -6C-20 -6 -28 -20 -26 -30C-10 -30 0 -20 0 -6Z" fill="${P.green}"/>
  <path d="M0 -12C18 -12 26 -26 24 -36C8 -36 0 -26 0 -12Z" fill="${P.sage}"/>
  <path d="M-16 6H16L11 30H-11Z" fill="${pot}"/><rect x="-18.5" y="2" width="37" height="7" rx="3.5" fill="${P.terraD}"/>`;

const fTree = () => `
  <rect x="-3.5" y="4" width="7" height="27" rx="3.5" fill="${P.terraD}"/>
  <circle cy="-8" r="23" fill="${P.green}"/><circle cx="-10" cy="-2" r="14" fill="${P.greenD}" opacity=".55"/>
  <circle cx="10" cy="-15" r="9" fill="${P.sage}" opacity=".8"/>`;

const fBin = (c, cD, glyph) => {
  const g = {
    leaf: G(0, 7, .6, fLeaf('#fff', '#e3ecdc')),
    drop: G(0, 7, .52, fDrop('#fff', '#cfe3ea')),
    dot: '<circle cy="7" r="5.5" fill="#fff"/>'
  }[glyph];
  return `<rect x="-6" y="-33" width="12" height="7" rx="3.5" fill="${cD}"/>
    <path d="M-15 -14H15L12 28Q12 31 9 31H-9Q-12 31 -12 28Z" fill="${c}"/>
    <rect x="-19" y="-26" width="38" height="11" rx="5.5" fill="${cD}"/>${g}`;
};

const fSolar = () => `
  <g transform="skewX(-14)"><rect x="-31" y="-21" width="62" height="40" rx="3" fill="${P.teal}"/>
  ${[0, 1, 2].flatMap(i => [0, 1].map(j => `<rect x="${-28 + i * 20}" y="${-18 + j * 19}" width="17" height="16" rx="1.5" fill="${P.tealM}"/>`)).join('')}</g>
  <rect x="-2.5" y="19" width="5" height="11" fill="${P.graphite}"/><rect x="-15" y="29" width="30" height="4" rx="2" fill="${P.graphite}"/>`;

const fSeesaw = () => `
  <path d="M-13 30H13L0 6Z" fill="${P.terraD}"/>
  <g transform="rotate(-11 0 6)"><rect x="-38" y="-2" width="76" height="9" rx="4.5" fill="${P.mustard}"/>
    <circle cx="-25" cy="-13" r="11" fill="${P.teal}"/><circle cx="28" cy="-7" r="5.5" fill="${P.terra}"/></g>`;

const fBoat = () => `
  <path d="M-26 -4H26L17 14H-17Z" fill="${P.terra}"/><path d="M-1 -8V-36L20 -8Z" fill="${P.mustard}"/>
  <path d="M-46 8Q-34 -1 -23 8T0 8T23 8T46 8V40H-46Z" fill="${P.tealM}" opacity=".95"/>
  <path d="M-46 20Q-34 11 -23 20T0 20T23 20T46 20V40H-46Z" fill="${P.teal}"/>`;

const fThermos = () => `
  <rect x="-12" y="-33" width="24" height="12" rx="4" fill="${P.terra}"/>
  <rect x="-16" y="-23" width="32" height="56" rx="9" fill="${P.tealM}"/>
  <rect x="-16" y="-3" width="32" height="7" fill="${P.cream}" opacity=".85"/>
  <rect x="-10" y="-17" width="5" height="44" rx="2.5" fill="#fff" opacity=".25"/>
  <circle cx="-4" cy="-40" r="2.6" fill="${P.sky}"/><circle cx="4" cy="-47" r="2" fill="${P.sky}"/>`;

const fRobot = () => `
  <rect x="-1.8" y="-31" width="3.6" height="11" fill="${P.graphite}"/><circle cy="-33" r="4.6" fill="${P.terra}"/>
  <rect x="-22" y="-20" width="44" height="31" rx="11" fill="${P.sky}"/>
  <circle cx="-8.5" cy="-5" r="4.6" fill="${P.navy}"/><circle cx="8.5" cy="-5" r="4.6" fill="${P.navy}"/>
  <rect x="-24.5" y="-12" width="5" height="12" rx="2.5" fill="${P.tealM}"/><rect x="19.5" y="-12" width="5" height="12" rx="2.5" fill="${P.tealM}"/>
  <rect x="-16" y="14" width="32" height="19" rx="7" fill="${P.tealM}"/><circle cy="23.5" r="4" fill="${P.mustard}"/>`;
