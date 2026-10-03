/* art.js — vẽ nhân vật và đồ vật bằng SVG thuần (không dùng ảnh ngoài).
   Mọi hàm trả về chuỗi SVG; tọa độ nhân vật: khung 100 x 150, chân ở y = 148. */
const OL = '#4a3426';                      // màu nét viền nâu đậm, mềm hơn màu đen
const SKIN = { a: '#ffdcc2', b: '#f6c9a6', c: '#e0a97f' };
const HAIR = { black: '#2a201d', brown: '#5a3b2e', dark: '#3a2a25' };

const G = (x, y, s, inner, rot = 0) =>
  `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">${inner}</g>`;

/* ---------- cánh tay: viền -> tay áo -> cẳng tay -> bàn tay ---------- */
function limb(sx, sy, hx, hy, sleeve, skin, w = 7.6) {
  const mx = sx + (hx - sx) * 0.52, my = sy + (hy - sy) * 0.52;
  return `<path d="M${sx} ${sy}L${hx} ${hy}" stroke="${OL}" stroke-width="${w + 3.6}" stroke-linecap="round" fill="none"/>
    <path d="M${sx} ${sy}L${mx} ${my}" stroke="${sleeve}" stroke-width="${w}" stroke-linecap="round" fill="none"/>
    <path d="M${mx} ${my}L${hx} ${hy}" stroke="${skin}" stroke-width="${w}" stroke-linecap="round" fill="none"/>
    <circle cx="${hx}" cy="${hy}" r="6" fill="${skin}" stroke="${OL}" stroke-width="2.2"/>`;
}

/* ---------- học sinh / cô giáo ---------- */
function kid(o = {}) {
  const d = Object.assign({
    skin: SKIN.a, hair: HAIR.black, style: 'boy', shirt: '#ffffff', pants: '#2f58a8',
    scarf: '#e63946', lh: [12, 100], rh: [88, 100], mouth: 'smile',
    specs: false, goggles: false, coat: false, bow: '#ff6b8a'
  }, o);
  const girl = d.style !== 'boy';
  const sleeve = d.coat ? '#ffffff' : d.shirt;
  const p = [];

  /* tóc phía sau */
  if (d.style === 'tails') {
    p.push(`<ellipse cx="50" cy="40" rx="31" ry="29" fill="${d.hair}"/>`);
    p.push(`<g transform="rotate(16 12 62)"><ellipse cx="11" cy="66" rx="9.5" ry="18" fill="${d.hair}" stroke="${OL}" stroke-width="2.2"/></g>`);
    p.push(`<g transform="rotate(-16 88 62)"><ellipse cx="89" cy="66" rx="9.5" ry="18" fill="${d.hair}" stroke="${OL}" stroke-width="2.2"/></g>`);
  } else if (d.style === 'pony') {
    p.push(`<ellipse cx="50" cy="40" rx="31" ry="29" fill="${d.hair}"/>`);
    p.push(`<g transform="rotate(-18 86 60)"><ellipse cx="88" cy="66" rx="9" ry="21" fill="${d.hair}" stroke="${OL}" stroke-width="2.2"/></g>`);
  } else if (d.style === 'bob') {
    p.push(`<path d="M17 40C11 64 19 76 32 71L68 71C81 76 89 64 83 40C80 10 20 10 17 40Z" fill="${d.hair}" stroke="${OL}" stroke-width="2.2" stroke-linejoin="round"/>`);
  } else if (d.style === 'bun') {
    p.push(`<circle cx="50" cy="5" r="11" fill="${d.hair}" stroke="${OL}" stroke-width="2.2"/>`);
    p.push(`<ellipse cx="50" cy="40" rx="31" ry="29" fill="${d.hair}"/>`);
  }

  /* thân dưới */
  if (d.coat) {
    p.push(`<rect x="35" y="118" width="13" height="26" rx="6" fill="#55627f" stroke="${OL}" stroke-width="2.4"/>
            <rect x="52" y="118" width="13" height="26" rx="6" fill="#55627f" stroke="${OL}" stroke-width="2.4"/>
            <ellipse cx="41" cy="145" rx="10" ry="4.6" fill="#3b3b4a" stroke="${OL}" stroke-width="2"/>
            <ellipse cx="59" cy="145" rx="10" ry="4.6" fill="#3b3b4a" stroke="${OL}" stroke-width="2"/>`);
  } else if (girl) {
    p.push(`<rect x="36" y="124" width="8" height="18" rx="4" fill="${d.skin}" stroke="${OL}" stroke-width="2.2"/>
            <rect x="56" y="124" width="8" height="18" rx="4" fill="${d.skin}" stroke="${OL}" stroke-width="2.2"/>
            <rect x="36" y="136" width="8" height="8" rx="2" fill="#fff" stroke="${OL}" stroke-width="2"/>
            <rect x="56" y="136" width="8" height="8" rx="2" fill="#fff" stroke="${OL}" stroke-width="2"/>
            <ellipse cx="40" cy="145" rx="9" ry="4.4" fill="#4b4f6a" stroke="${OL}" stroke-width="2"/>
            <ellipse cx="60" cy="145" rx="9" ry="4.4" fill="#4b4f6a" stroke="${OL}" stroke-width="2"/>
            <path d="M31 112L69 112L77 134L23 134Z" fill="${d.pants}" stroke="${OL}" stroke-width="2.4" stroke-linejoin="round"/>`);
  } else {
    p.push(`<rect x="34" y="112" width="14" height="31" rx="6" fill="${d.pants}" stroke="${OL}" stroke-width="2.4"/>
            <rect x="52" y="112" width="14" height="31" rx="6" fill="${d.pants}" stroke="${OL}" stroke-width="2.4"/>
            <ellipse cx="41" cy="145" rx="10" ry="4.6" fill="#4b4f6a" stroke="${OL}" stroke-width="2"/>
            <ellipse cx="59" cy="145" rx="10" ry="4.6" fill="#4b4f6a" stroke="${OL}" stroke-width="2"/>`);
  }

  /* thân trên */
  if (d.coat) {
    p.push(`<rect x="27" y="75" width="46" height="60" rx="13" fill="#ffffff" stroke="${OL}" stroke-width="2.4"/>
            <path d="M42 76L50 102L58 76" fill="none" stroke="${OL}" stroke-width="2.2" stroke-linejoin="round"/>
            <circle cx="50" cy="112" r="2" fill="${OL}"/><circle cx="50" cy="123" r="2" fill="${OL}"/>
            <rect x="55" y="112" width="12" height="11" rx="2" fill="none" stroke="${OL}" stroke-width="1.8"/>
            <path d="M44 76L50 84L56 76Z" fill="${d.scarf}" stroke="${OL}" stroke-width="1.8"/>`);
  } else {
    p.push(`<rect x="30" y="76" width="40" height="42" rx="12" fill="${d.shirt}" stroke="${OL}" stroke-width="2.4"/>
            <path d="M36 77L64 77L50 103Z" fill="${d.scarf}" stroke="${OL}" stroke-width="2.2" stroke-linejoin="round"/>
            <circle cx="50" cy="80" r="3.8" fill="${d.scarf}" stroke="${OL}" stroke-width="1.8"/>`);
  }

  /* tay */
  p.push(limb(33, 85, d.lh[0], d.lh[1], sleeve, d.skin));
  p.push(limb(67, 85, d.rh[0], d.rh[1], sleeve, d.skin));

  /* đầu */
  p.push(`<circle cx="21" cy="44" r="5.2" fill="${d.skin}" stroke="${OL}" stroke-width="2"/>
          <circle cx="79" cy="44" r="5.2" fill="${d.skin}" stroke="${OL}" stroke-width="2"/>
          <ellipse cx="50" cy="40" rx="29" ry="27" fill="${d.skin}" stroke="${OL}" stroke-width="2.4"/>`);

  /* mặt */
  p.push(`<ellipse cx="29.5" cy="55" rx="5.6" ry="3.3" fill="#ff9fa8" opacity=".7"/>
          <ellipse cx="70.5" cy="55" rx="5.6" ry="3.3" fill="#ff9fa8" opacity=".7"/>
          <ellipse cx="38" cy="46" rx="4.4" ry="5.6" fill="#2b1d18"/><ellipse cx="62" cy="46" rx="4.4" ry="5.6" fill="#2b1d18"/>
          <circle cx="36.6" cy="43.6" r="1.8" fill="#fff"/><circle cx="60.6" cy="43.6" r="1.8" fill="#fff"/>
          <circle cx="39.6" cy="48.4" r=".9" fill="#fff"/><circle cx="63.6" cy="48.4" r=".9" fill="#fff"/>
          <path d="M32.5 36.5Q38 33.5 43 36" stroke="${d.hair}" stroke-width="1.9" fill="none" stroke-linecap="round"/>
          <path d="M57 36Q62 33.5 67.5 36.5" stroke="${d.hair}" stroke-width="1.9" fill="none" stroke-linecap="round"/>
          <path d="M49 51q1 2 2 0" stroke="#c98d6c" stroke-width="1.4" fill="none" stroke-linecap="round"/>`);
  if (d.mouth === 'open') {
    p.push(`<path d="M42.5 55Q50 70 57.5 55Z" fill="#d94a52" stroke="#8a3030" stroke-width="1.6" stroke-linejoin="round"/>
            <ellipse cx="50" cy="61.5" rx="3.6" ry="2.2" fill="#ff8a95"/>`);
  } else {
    p.push(`<path d="M43 56Q50 63 57 56" stroke="#8a3a3a" stroke-width="2" fill="none" stroke-linecap="round"/>`);
  }

  /* tóc phía trước */
  p.push(`<path d="M19 42C13 13 34 4 50 4C67 4 87 13 81 42C78 31 71 25 63 27C57 21 45 21 39 27C30 24 22 31 19 42Z" fill="${d.hair}" stroke="${OL}" stroke-width="2.2" stroke-linejoin="round"/>
          <path d="M33 12Q43 8 52 9" stroke="#fff" stroke-opacity=".28" stroke-width="3" fill="none" stroke-linecap="round"/>`);
  if (girl && d.style !== 'bun') {
    p.push(`<path d="M19 42C17 53 20 61 25 65C23 55 25 47 27 41Z" fill="${d.hair}" stroke="${OL}" stroke-width="1.8" stroke-linejoin="round"/>
            <path d="M81 42C83 53 80 61 75 65C77 55 75 47 73 41Z" fill="${d.hair}" stroke="${OL}" stroke-width="1.8" stroke-linejoin="round"/>`);
  }
  if (d.style === 'tails') {
    p.push(`<circle cx="18" cy="45" r="5" fill="${d.bow}" stroke="${OL}" stroke-width="1.8"/><circle cx="82" cy="45" r="5" fill="${d.bow}" stroke="${OL}" stroke-width="1.8"/>`);
  } else if (d.style === 'pony') {
    p.push(`<circle cx="84" cy="48" r="5" fill="${d.bow}" stroke="${OL}" stroke-width="1.8"/>`);
  }

  /* kính */
  if (d.specs) {
    p.push(`<circle cx="38" cy="46" r="8.6" fill="#ffffff" fill-opacity=".25" stroke="#35354a" stroke-width="2.2"/>
            <circle cx="62" cy="46" r="8.6" fill="#ffffff" fill-opacity=".25" stroke="#35354a" stroke-width="2.2"/>
            <path d="M46.6 45h6.8M29.4 44L22 42M70.6 44L78 42" stroke="#35354a" stroke-width="2" fill="none" stroke-linecap="round"/>`);
  }
  if (d.goggles) {
    p.push(`<path d="M22 44H29M71 44H78" stroke="#2f6fd0" stroke-width="3.4" stroke-linecap="round"/>
            <ellipse cx="38" cy="46" rx="9.6" ry="8" fill="#a8dcff" fill-opacity=".55" stroke="#2f6fd0" stroke-width="2.6"/>
            <ellipse cx="62" cy="46" rx="9.6" ry="8" fill="#a8dcff" fill-opacity=".55" stroke="#2f6fd0" stroke-width="2.6"/>
            <path d="M47.5 46h5" stroke="#2f6fd0" stroke-width="3" stroke-linecap="round"/>
            <path d="M32 43Q35 40.5 39 41" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity=".85"/>`);
  }
  return `<g>${p.join('')}</g>`;
}
const K = (o, x, y, s = 1) => G(x, y, s, kid(o));

/* ---------- đồ vật ---------- */
const sw = (w = 2) => `stroke="${OL}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

const apple = (x, y, s = 1) => G(x, y, s, `
  <path d="M0 -7C-11 -13 -18 2 -12 12C-8 19 -3 17 0 15C3 17 8 19 12 12C18 2 11 -13 0 -7Z" fill="#e84545" ${sw(2)}/>
  <path d="M0 -7Q1 -13 5 -16" fill="none" ${sw(2)}/>
  <path d="M3 -11Q10 -17 15 -12Q9 -6 3 -11Z" fill="#58b34a" ${sw(1.6)}/>
  <path d="M-8 -1Q-9 5 -6 9" stroke="#fff" stroke-opacity=".7" stroke-width="2.6" fill="none" stroke-linecap="round"/>`);
const orange = (x, y, s = 1) => G(x, y, s, `
  <circle r="12" fill="#ffa630" ${sw(2)}/><circle cx="-4" cy="-4" r="2" fill="#ffd08a"/>
  <path d="M0 -12Q5 -18 10 -14Q5 -9 0 -12Z" fill="#58b34a" ${sw(1.5)}/>`);
const banana = (x, y, s = 1) => G(x, y, s, `
  <path d="M-16 -4Q-4 12 16 -8Q14 6 -2 12Q-14 12 -16 -4Z" fill="#ffd93d" ${sw(2)}/>
  <path d="M16 -8L19 -12" ${sw(2.6)} fill="none"/>`);
const carrot = (x, y, s = 1, rot = 0) => G(x, y, s, `
  <path d="M-6 -8L6 -8L0 22Z" fill="#ff8a2b" ${sw(2)}/><path d="M-3 0H2M-2 8H1" stroke="#c4600f" stroke-width="1.4"/>
  <path d="M0 -8Q-6 -18 -3 -22M0 -8Q0 -20 2 -24M0 -8Q6 -16 8 -20" fill="none" stroke="#3f9e3f" stroke-width="3" stroke-linecap="round"/>`, rot);
const broccoli = (x, y, s = 1) => G(x, y, s, `
  <rect x="-4" y="2" width="8" height="12" rx="2" fill="#8bc34a" ${sw(1.8)}/>
  <circle cx="-8" cy="-2" r="8" fill="#43a047" ${sw(1.8)}/><circle cx="8" cy="-2" r="8" fill="#43a047" ${sw(1.8)}/><circle cx="0" cy="-8" r="9" fill="#4caf50" ${sw(1.8)}/>`);
const bottle = (x, y, s = 1, color = '#8fd0f2') => G(x, y, s, `
  <rect x="-8" y="-14" width="16" height="32" rx="6" fill="${color}" ${sw(2)}/>
  <rect x="-4.5" y="-22" width="9" height="8" rx="2" fill="#3a86d6" ${sw(1.8)}/>
  <path d="M-8 -2H8M-8 8H8" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>
  <path d="M-4 -10V14" stroke="#fff" stroke-opacity=".6" stroke-width="2.4" stroke-linecap="round"/>`);

const heart = (x, y, s = 1, c = '#ff6b8a', rot = 0) => G(x, y, s, `<path d="M0 8C-12 0 -12 -10 -6 -11C-3 -11.6 -1 -10 0 -8C1 -10 3 -11.6 6 -11C12 -10 12 0 0 8Z" fill="${c}" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/>`, rot);
const sparkle = (x, y, s = 1, c = '#ffd23f') => G(x, y, s, `<path d="M0 -9Q1.4 -1.4 9 0Q1.4 1.4 0 9Q-1.4 1.4 -9 0Q-1.4 -1.4 0 -9Z" fill="${c}" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/>`);
const star = (x, y, s = 1, c = '#ffd23f', rot = 0) => G(x, y, s, `<path d="M0 -10L3 -3.4L10 -3L4.6 1.8L6.2 9L0 5.2L-6.2 9L-4.6 1.8L-10 -3L-3 -3.4Z" fill="${c}" ${sw(1.6)}/>`, rot);
const cloud = (x, y, s = 1, c = '#fff') => G(x, y, s, `<g fill="${c}"><circle cx="-14" cy="2" r="9"/><circle cx="-2" cy="-4" r="12"/><circle cx="12" cy="0" r="10"/><rect x="-22" y="2" width="42" height="9" rx="4.5"/></g>`);

const bulb = (x, y, s = 1, lit = true) => G(x, y, s, `
  ${lit ? `<circle cx="0" cy="-6" r="26" fill="#fff3a0" fill-opacity=".55"/>
  <g stroke="#ffc83d" stroke-width="3" stroke-linecap="round"><path d="M0 -38V-33M-24 -30L-20 -26M24 -30L20 -26M-32 -6H-27M32 -6H27"/></g>` : ''}
  <path d="M-6 10C-6 4 -14 1 -14 -8A14 14 0 1 1 14 -8C14 1 6 4 6 10Z" fill="${lit ? '#ffe066' : '#e6ecf2'}" ${sw(2)}/>
  <path d="M-4 9V0L0 -5L4 0V9" fill="none" stroke="#c98a1c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="-6.5" y="10" width="13" height="8" rx="2.4" fill="#b8bcc4" ${sw(1.8)}/>
  <path d="M-6 14H6" stroke="${OL}" stroke-width="1.2"/>
  <path d="M-9 -12Q-9 -17 -4 -19" stroke="#fff" stroke-opacity=".8" stroke-width="2.4" fill="none" stroke-linecap="round"/>`);

const sunny = (x, y, r = 12) => `
  <g transform="translate(${x} ${y})"><g stroke="#ffb92e" stroke-width="3.2" stroke-linecap="round">
    ${[0, 45, 90, 135, 180, 225, 270, 315].map(a => `<path d="M0 ${-r - 5}V${-r - 10}" transform="rotate(${a})"/>`).join('')}</g>
  <circle r="${r}" fill="#ffd23f" ${sw(2)}/><circle cx="-4" cy="-2" r="1.5" fill="${OL}"/><circle cx="4" cy="-2" r="1.5" fill="${OL}"/>
  <path d="M-4 3Q0 7 4 3" fill="none" stroke="${OL}" stroke-width="1.5" stroke-linecap="round"/></g>`;

const turbine = (x, y, s = 1) => G(x, y, s, `
  <path d="M-3 0L3 0L1.4 -44L-1.4 -44Z" fill="#fff" ${sw(1.8)}/>
  <g transform="translate(0 -44)">
    ${[0, 120, 240].map(a => `<ellipse cx="0" cy="-12" rx="3.2" ry="13" fill="#fff" ${sw(1.6)} transform="rotate(${a})"/>`).join('')}
    <circle r="4" fill="#ff8a65" ${sw(1.6)}/></g>`);

const solar = (x, y, s = 1) => G(x, y, s, `
  <path d="M0 8V26M-10 26H10" ${sw(2.4)} fill="none"/>
  <path d="M-28 10L-18 -14H30L20 10Z" fill="#3a6fc4" ${sw(2.2)}/>
  <path d="M-23 -2H25M-8 -14L-13 10M7 -14L2 10M20 -14L16 10M-26 4H22" stroke="#cfe5ff" stroke-width="1.4"/>
  <path d="M-14 -11L-8 -11" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>`);

const flask = (x, y, s = 1, c = '#7be07b') => G(x, y, s, `
  <path d="M-10.8 4H10.8L16 14Q18 20 11 20H-11Q-18 20 -16 14Z" fill="${c}"/>
  <path d="M-5 -16H5V-6L16 14Q19 21 11 21H-11Q-19 21 -16 14L-5 -6Z" fill="${c}" fill-opacity="0" ${sw(2.2)}/>
  <path d="M-7 -16H7" ${sw(2.6)} fill="none"/>
  <circle cx="-3" cy="10" r="2" fill="#fff" fill-opacity=".8"/><circle cx="4" cy="14" r="1.6" fill="#fff" fill-opacity=".8"/>
  <path d="M-12 11Q-13 14 -11 16" stroke="#fff" stroke-opacity=".6" stroke-width="2" fill="none" stroke-linecap="round"/>`);
const bubbles = (x, y, s = 1) => G(x, y, s, `<g fill="#fff" fill-opacity=".75" stroke="#7a6ac4" stroke-width="1.2"><circle cx="0" cy="0" r="3.4"/><circle cx="7" cy="-8" r="2.4"/><circle cx="-5" cy="-11" r="2.8"/><circle cx="3" cy="-17" r="1.8"/></g>`);
const tube = (x, y, s = 1, c = '#ff7aa8') => G(x, y, s, `
  <path d="M-4 -4H4V12A4 4 0 0 1 -4 12Z" fill="${c}"/>
  <path d="M-4 -18V12A4 4 0 0 0 4 12V-18" fill="none" ${sw(2)}/><path d="M-6 -18H6" ${sw(2.4)} fill="none"/>`);
const beaker = (x, y, s = 1, c = '#ffd166') => G(x, y, s, `
  <path d="M-11 -2H11V14A4 4 0 0 1 7 18H-7A4 4 0 0 1 -11 14Z" fill="${c}"/>
  <path d="M-13 -14H13M-11 -14V14A4 4 0 0 0 -7 18H7A4 4 0 0 0 11 14V-14" fill="none" ${sw(2.2)}/>
  <path d="M-11 -6H-5M-11 2H-5M-11 10H-5" stroke="${OL}" stroke-width="1.5"/>`);
const lemon = (x, y, s = 1) => G(x, y, s, `
  <ellipse rx="13" ry="10" fill="#f3c623" ${sw(2)}/><ellipse rx="9.6" ry="7" fill="#fbe97c"/>
  <path d="M0 0L9 0M0 0L6 5M0 0L0 6.4M0 0L-6 5M0 0L-9 0M0 0L-6 -5M0 0L0 -6.4M0 0L6 -5" stroke="#f3c623" stroke-width="1.8" stroke-linecap="round"/>`);
const jar = (x, y, s = 1) => G(x, y, s, `
  <rect x="-10" y="-12" width="20" height="26" rx="4" fill="#fff" ${sw(2)}/><rect x="-11.5" y="-17" width="23" height="7" rx="2.5" fill="#6aa7e8" ${sw(1.8)}/>
  <rect x="-7" y="-4" width="14" height="10" rx="2" fill="#ffe8a3"/><text x="0" y="3.4" font-family="Nunito" font-weight="800" font-size="5.4" text-anchor="middle" fill="#7a4a0a">SODA</text>`);
const molecule = (x, y, s = 1) => G(x, y, s, `
  <path d="M-14 8L0 -4L14 8M0 -4V-18" stroke="${OL}" stroke-width="2.4" fill="none"/>
  <circle cx="0" cy="-4" r="7" fill="#ef5350" ${sw(1.8)}/><circle cx="-14" cy="8" r="5.4" fill="#fff" ${sw(1.8)}/><circle cx="14" cy="8" r="5.4" fill="#fff" ${sw(1.8)}/>
  <circle cx="0" cy="-18" r="5.4" fill="#42a5f5" ${sw(1.8)}/>`);

const sapling = (x, y, s = 1) => G(x, y, s, `
  <path d="M-12 4H12L9 22H-9Z" fill="#c9824a" ${sw(2)}/><path d="M-13 0H13V6H-13Z" fill="#dc9a60" ${sw(2)}/>
  <path d="M0 0V-14" stroke="#3f8f3f" stroke-width="3" stroke-linecap="round"/>
  <path d="M0 -10Q-14 -10 -15 -22Q-2 -22 0 -10Z" fill="#5ec26a" ${sw(1.8)}/><path d="M0 -14Q13 -14 15 -26Q2 -26 0 -14Z" fill="#7ad47f" ${sw(1.8)}/>`);
const tree = (x, y, s = 1) => G(x, y, s, `
  <path d="M-4 0V-22H4V0Z" fill="#a9754a" ${sw(2)}/>
  <circle cx="0" cy="-34" r="17" fill="#5ec26a" ${sw(2)}/><circle cx="-12" cy="-26" r="11" fill="#6fd078" ${sw(2)}/><circle cx="12" cy="-27" r="11" fill="#4fb85a" ${sw(2)}/>
  <circle cx="-4" cy="-38" r="3" fill="#fff" fill-opacity=".35"/>`);
const globe = (x, y, r = 16) => `<g transform="translate(${x} ${y})">
  <circle r="${r}" fill="#4aa3e8" ${sw(2.2)}/>
  <path d="M-8 -9Q-2 -14 4 -9Q8 -5 2 -2Q-2 2 -6 -1Q-12 -3 -8 -9Z" fill="#6cc46a"/><path d="M4 4Q10 2 12 8Q9 13 3 12Q0 8 4 4Z" fill="#6cc46a"/>
  <path d="M-9 -8Q-9 -12 -5 -14" stroke="#fff" stroke-opacity=".8" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>`;
const leaf = (x, y, s = 1, c = '#fff', rot = 0) => G(x, y, s, `<path d="M0 8C-9 4 -9 -8 0 -12C9 -8 9 4 0 8Z" fill="${c}"/><path d="M0 8V-8" stroke="rgba(0,0,0,.25)" stroke-width="1.4"/>`, rot);

/* thùng rác phân loại: mặt trước y từ 0 đến h, rộng w, tâm ở x */
function bin(x, y, w, h, c, icon) {
  const ic = {
    leaf: leaf(0, h * 0.52, 1.5),
    loop: `<g transform="translate(0 ${h * 0.52})" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M-7 3A8 8 0 0 1 3 -7"/><path d="M7 -3A8 8 0 0 1 -3 7"/><path d="M3 -11L5 -6L0 -6Z M-3 11L-5 6L0 6Z" fill="#fff" stroke="none"/></g>`,
    dot: `<g transform="translate(0 ${h * 0.52})" fill="#fff"><circle r="4.5"/><rect x="-7" y="-9" width="14" height="3" rx="1.5"/></g>`
  }[icon];
  return `<g transform="translate(${x} ${y})">
    <path d="M${-w / 2} 0L${w / 2} 0L${w / 2 - 3} ${h}L${-w / 2 + 3} ${h}Z" fill="${c}" ${sw(2.2)}/>
    <rect x="${-w / 2 - 3}" y="-7" width="${w + 6}" height="8" rx="3" fill="${c}" ${sw(2.2)}/><rect x="${-w / 5}" y="-11" width="${w * 0.4}" height="5" rx="2" fill="${c}" ${sw(1.8)}/>
    <path d="M${-w / 2 + 6} 6V${h - 6}" stroke="#fff" stroke-opacity=".3" stroke-width="3" stroke-linecap="round"/>${ic}</g>`;
}

const robot = (x, y, s = 1) => G(x, y, s, `
  <path d="M0 -26V-19" ${sw(2)} fill="none"/><circle cy="-28" r="3.4" fill="#ef5350" ${sw(1.6)}/>
  <rect x="-15" y="-19" width="30" height="22" rx="8" fill="#dfe7f5" ${sw(2.2)}/>
  <rect x="-10" y="-14" width="20" height="12" rx="5" fill="#26324d"/><circle cx="-4.4" cy="-8" r="2.6" fill="#5ee6ff"/><circle cx="4.4" cy="-8" r="2.6" fill="#5ee6ff"/>
  <rect x="-18" y="-12" width="4" height="8" rx="2" fill="#9fb4d6" ${sw(1.4)}/><rect x="14" y="-12" width="4" height="8" rx="2" fill="#9fb4d6" ${sw(1.4)}/>
  <rect x="-11" y="5" width="22" height="17" rx="6" fill="#9fb4d6" ${sw(2.2)}/><circle cy="13" r="3.4" fill="#ffd23f" ${sw(1.4)}/>
  <path d="M-11 9L-17 15M11 9L17 15" ${sw(2.6)} fill="none"/>`);

const laptop = (x, y, s = 1) => G(x, y, s, `
  <rect x="-24" y="-30" width="48" height="32" rx="3.5" fill="#2b3a5c" ${sw(2.2)}/>
  <path d="M-18 -23H-6M-18 -17H4M-12 -11H8M-18 -5H-8" stroke="#6ee7a8" stroke-width="2" stroke-linecap="round"/><path d="M6 -23H16M10 -17H18" stroke="#ffd23f" stroke-width="2" stroke-linecap="round"/>
  <path d="M-30 2H30L26 8H-26Z" fill="#c9d2e3" ${sw(2)}/>`);

function gear(x, y, r = 12, c = '#ffb300', rot = 0) {
  const t = Array.from({ length: 8 }, (_, i) => `<rect x="${-r * 0.2}" y="${-r - 3.4}" width="${r * 0.4}" height="${r * 0.55}" rx="1.4" fill="${c}" ${sw(1.6)} transform="rotate(${i * 45})"/>`).join('');
  return `<g transform="translate(${x} ${y}) rotate(${rot})">${t}<circle r="${r}" fill="${c}" ${sw(2)}/><circle r="${r * 0.42}" fill="#fff8e1" ${sw(1.8)}/></g>`;
}

const rocket = (x, y, s = 1, rot = 0) => G(x, y, s, `
  <path d="M-6 16Q0 38 6 16Z" fill="#ffb02e" ${sw(1.8)}/><path d="M-3 16Q0 28 3 16Z" fill="#fff2a8"/>
  <path d="M-9 4L-19 20L-8 15Z" fill="#ef5350" ${sw(1.8)}/><path d="M9 4L19 20L8 15Z" fill="#ef5350" ${sw(1.8)}/>
  <path d="M0 -32C13 -19 13 5 9 16H-9C-13 5 -13 -19 0 -32Z" fill="#fff" ${sw(2.2)}/>
  <path d="M0 -32C6 -26 10 -21 11 -14H-11C-10 -21 -6 -26 0 -32Z" fill="#ef5350" ${sw(2)}/>
  <circle cy="-4" r="5.6" fill="#8fd3ff" ${sw(2)}/><circle cx="-1.6" cy="-5.6" r="1.6" fill="#fff"/>`, rot);

const planet = (x, y, r = 10) => `<g transform="translate(${x} ${y})">
  <ellipse rx="${r * 1.9}" ry="${r * 0.5}" fill="none" stroke="#f0a35e" stroke-width="3.2" transform="rotate(-20)"/>
  <circle r="${r}" fill="#ffc979" ${sw(2)}/><path d="M${-r * .7} ${-r * .2}Q0 ${-r * .5} ${r * .7} ${-r * .2}" stroke="#f0a35e" stroke-width="2" fill="none"/>
  <ellipse rx="${r * 1.9}" ry="${r * 0.5}" fill="none" stroke="#f0a35e" stroke-width="3.2" transform="rotate(-20)" stroke-dasharray="${r * 3.4} ${r * 20}" stroke-dashoffset="${-r * 3.2}"/></g>`;

const telescope = (x, y, s = 1, rot = -35) => G(x, y, s, `
  <path d="M0 8L-8 28M0 8L8 28M0 8V28" ${sw(2.2)} fill="none"/>
  <g transform="rotate(${rot})"><rect x="-6" y="-26" width="12" height="38" rx="4" fill="#5b8bd6" ${sw(2)}/><rect x="-8" y="-32" width="16" height="10" rx="3" fill="#2f5fa8" ${sw(2)}/><rect x="-4" y="12" width="8" height="8" rx="2" fill="#2f5fa8" ${sw(1.8)}/></g>`);

const megaphone = (c = '#e8579a') => `<svg viewBox="0 0 32 32" width="28" height="28"><path d="M4 12L20 5V25L4 18Z" fill="${c}" stroke="${OL}" stroke-width="1.6" stroke-linejoin="round"/><rect x="2" y="11" width="5" height="8" rx="2" fill="#ffd166" stroke="${OL}" stroke-width="1.4"/><path d="M8 18L10 27H14L13 22.5" fill="${c}" stroke="${OL}" stroke-width="1.4" stroke-linejoin="round"/><path d="M24 11Q28 15 24 19M26 8Q32 15 26 22" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round"/></svg>`;

/* nền tròn mềm cho mỗi tranh minh họa (khung 220 x 210) */
const blob = (c1, c2) => `
  <path d="M16 112C6 62 56 14 116 14C178 14 214 62 207 120C200 172 152 204 104 202C52 200 26 162 16 112Z" fill="${c1}"/>
  <path d="M30 112C24 70 66 30 116 30C168 30 196 70 191 118C186 160 146 186 104 184C62 182 38 150 30 112Z" fill="${c2}" fill-opacity=".75"/>`;
const scene = inner => `<svg viewBox="0 0 220 210" xmlns="http://www.w3.org/2000/svg" font-family="Nunito, sans-serif">${inner}</svg>`;
