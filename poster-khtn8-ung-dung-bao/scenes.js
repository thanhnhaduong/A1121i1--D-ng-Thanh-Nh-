/* scenes.js — 6 tranh minh họa + các chi tiết trang trí của poster (đều là SVG vẽ tay bằng mã). */

/* quầy/bàn phía trước: che phần chân nhân vật, có dòng chữ khẩu hiệu */
const counter = (label, c1 = '#f2c98d', c2 = '#e0a867') => `
  <rect x="6" y="158" width="208" height="13" rx="6" fill="${c1}" ${sw(2.2)}/>
  <rect x="13" y="170" width="194" height="38" rx="3" fill="${c2}" ${sw(2.2)}/>
  <text x="110" y="195" text-anchor="middle" font-family="Baloo 2" font-weight="800" font-size="15" fill="#fff" stroke="${OL}" stroke-width="3" paint-order="stroke" letter-spacing=".5">${label}</text>`;

const battery = (x, y, s = 1) => G(x, y, s, `
  <rect x="-14" y="-9" width="26" height="18" rx="4" fill="#66c36e" ${sw(2)}/><rect x="12" y="-4" width="4" height="8" rx="1.6" fill="#b8bcc4" ${sw(1.6)}/>
  <path d="M-2 -6L-7 1H-1L-3 6L3 -1H-2Z" fill="#fff59d" stroke="${OL}" stroke-width="1.2" stroke-linejoin="round"/>`);
const plug = (x, y, s = 1) => G(x, y, s, `
  <path d="M-8 -4H8V6A8 8 0 0 1 -8 6Z" fill="#e8e8ee" ${sw(2)}/><path d="M-4 -4V-12M4 -4V-12" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>
  <path d="M0 14Q0 22 8 22" fill="none" stroke="${OL}" stroke-width="2.4" stroke-linecap="round"/>`);
const chip = (x, y, s = 1) => G(x, y, s, `
  <g stroke="${OL}" stroke-width="2.2" stroke-linecap="round">${[-10, -3, 4, 11].map(v => `<path d="M${v} -16V-21M${v} 16V21M-16 ${v}H-21M16 ${v}H21"/>`).join('')}</g>
  <rect x="-15" y="-15" width="30" height="30" rx="6" fill="#3a6fc4" ${sw(2.2)}/>
  <text y="6" text-anchor="middle" font-family="Baloo 2" font-weight="800" font-size="17" fill="#fff">AI</text>`);
const pcb = (x, y, s = 1) => G(x, y, s, `
  <rect x="-18" y="-11" width="36" height="22" rx="3" fill="#43a047" ${sw(2)}/>
  <path d="M-12 -4H-2V4H8M-12 4H-6M2 -6H12" stroke="#c8e6c9" stroke-width="1.6" fill="none"/>
  <circle cx="12" cy="4" r="2" fill="#ffd54f"/><circle cx="-12" cy="-4" r="2" fill="#ffd54f"/><rect x="-1" y="-8" width="8" height="6" rx="1" fill="#263238"/>`);
const phScale = (x, y, s = 1) => G(x, y, s, `
  <rect x="-32" y="-9" width="64" height="18" rx="9" fill="#fff" ${sw(2)}/>
  <rect x="-28" y="-5" width="56" height="10" rx="5" fill="url(#phg)"/>
  <text x="0" y="-13" text-anchor="middle" font-family="Baloo 2" font-weight="800" font-size="13" fill="#6a3fb0">pH 0 – 14</text>`);
const atom = (x, y, s = 1) => G(x, y, s, `
  <g fill="none" stroke="#6a3fb0" stroke-width="2.2"><ellipse rx="17" ry="6.5"/><ellipse rx="17" ry="6.5" transform="rotate(60)"/><ellipse rx="17" ry="6.5" transform="rotate(120)"/></g>
  <circle r="4.2" fill="#ef5350" ${sw(1.4)}/><circle cx="17" r="2.8" fill="#42a5f5"/><circle cx="-8.5" cy="-14.7" r="2.8" fill="#42a5f5"/><circle cx="-8.5" cy="14.7" r="2.8" fill="#42a5f5"/>`);
const wifi = (x, y, s = 1, c = '#2f7fd6') => G(x, y, s, `<g fill="none" stroke="${c}" stroke-width="3.2" stroke-linecap="round"><path d="M-14 -4Q0 -16 14 -4"/><path d="M-9 2Q0 -6 9 2"/></g><circle cy="9" r="2.6" fill="${c}"/>`);
const boat = (x, y, s = 1) => G(x, y, s, `<path d="M-14 4H14L9 12H-9Z" fill="#ff8a65" ${sw(1.8)}/><path d="M0 4V-14L11 2Z" fill="#fff" ${sw(1.8)}/>`);

/* ===== 1. Sức khỏe & dinh dưỡng ===== */
const scene1 = () => scene(`
  ${blob('#ffc9de', '#ffe6f0')}
  <path d="M30 40H78L86 26L96 52L104 36H190" fill="none" stroke="#f0689a" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
  ${heart(110, 26, 2.4, '#ff6b8a')}${sparkle(30, 70, 1.1)}${sparkle(196, 66, 1.2, '#fff')}${star(186, 28, 1, '#ffd23f', 12)}
  ${apple(99, 84, 1.05)}${bottle(124, 92, 1.05)}
  ${K({ style: 'tails', lh: [8, 56], rh: [88, 44], mouth: 'open' }, 12, 60, .92)}
  ${K({ style: 'boy', lh: [12, 54], rh: [90, 44], mouth: 'open' }, 116, 60, .92)}
  ${counter('ĂN KHỎE – SỐNG KHỎE', '#f7d9a0', '#e8b26a')}
  ${broccoli(30, 150, 1.15)}${carrot(58, 149, 1.0, -22)}${orange(168, 148, 1.1)}${banana(196, 150, .85)}
`);

/* ===== 2. Năng lượng & điện an toàn ===== */
const scene2 = () => scene(`
  ${blob('#ffdca0', '#fff1d0')}
  ${sunny(190, 34, 13)}${turbine(28, 76, .95)}${solar(140, 40, .85)}${sparkle(80, 30, 1.1, '#fff')}${cloud(100, 18, .6)}
  ${bulb(108, 88, 1.05)}
  ${K({ style: 'boy', hair: HAIR.brown, lh: [6, 70], rh: [90, 44], mouth: 'open' }, 14, 62, .9)}
  ${K({ style: 'pony', lh: [10, 44], rh: [94, 70], mouth: 'open' }, 112, 62, .9)}
  ${counter('TIẾT KIỆM ĐIỆN', '#f7d9a0', '#e8b26a')}
  ${battery(46, 150, 1.25)}${plug(172, 147, 1.15)}
`);

/* ===== 3. Hóa học quanh ta ===== */
const scene3 = () => scene(`
  <defs><linearGradient id="phg" x1="0" x2="1"><stop offset="0" stop-color="#e8312f"/><stop offset=".25" stop-color="#fbb12a"/><stop offset=".5" stop-color="#6fc46c"/><stop offset=".75" stop-color="#2f8bc9"/><stop offset="1" stop-color="#5a3f9e"/></linearGradient></defs>
  ${blob('#dcc9f5', '#f1e9fc')}
  ${molecule(36, 40, 1.05)}${phScale(110, 36, 1)}${atom(184, 40, 1.1)}${sparkle(62, 72, 1, '#fff')}
  ${flask(92, 96, 1.05, '#7be07b')}${bubbles(92, 76)}${tube(127, 98, 1.35, '#ff7aa8')}${bubbles(127, 78, .8)}
  ${K({ style: 'bob', hair: HAIR.brown, skin: SKIN.b, goggles: true, lh: [14, 100], rh: [86, 50], mouth: 'open' }, 12, 60, .92)}
  ${K({ style: 'boy', skin: SKIN.a, goggles: true, coat: true, lh: [12, 50], rh: [88, 100], mouth: 'open' }, 116, 60, .92)}
  ${counter('HÓA HỌC VUI', '#f7d9a0', '#e8b26a')}
  ${lemon(40, 151, 1.2)}${beaker(110, 148, 1.2, '#ffd166')}${jar(176, 149, 1.15)}
`);

/* ===== 4. Môi trường xanh ===== */
const scene4 = () => scene(`
  ${blob('#c4e8c6', '#e6f6e4')}
  ${globe(110, 34, 17)}${heart(124, 20, .8, '#ff6b8a')}${tree(26, 84, .85)}${cloud(180, 28, .8)}${sparkle(70, 30, 1, '#fff')}${leaf(160, 56, 1, '#6fd078', 25)}
  ${bottle(101, 80, 1.0, '#9fd8f5')}${banana(124, 84, 1.05)}
  ${K({ style: 'pony', hair: HAIR.dark, lh: [10, 70], rh: [90, 38], mouth: 'open' }, 10, 60, .92)}
  ${K({ style: 'boy', hair: HAIR.brown, skin: SKIN.b, lh: [10, 40], rh: [92, 70], mouth: 'open' }, 118, 60, .92)}
  <path d="M6 176Q110 158 214 176V208H6Z" fill="#9ccf8a" ${sw(2.2)}/>
  ${bin(52, 144, 40, 58, '#2f7fd6', 'loop')}${bin(110, 144, 40, 58, '#78909c', 'dot')}${bin(168, 144, 40, 58, '#43a047', 'leaf')}
`);

/* ===== 5. Công nghệ & kỹ thuật ===== */
const scene5 = () => scene(`
  ${blob('#c9defa', '#e8f2fe')}
  ${gear(36, 40, 16)}${gear(64, 58, 10, '#4fc3f7', 15)}${wifi(110, 34, 1.2)}${chip(184, 38, 1)}${sparkle(150, 22, 1, '#fff')}
  ${gear(197, 92, 10, '#ffb300', 8)}
  ${K({ style: 'tails', hair: HAIR.brown, specs: true, lh: [6, 62], rh: [94, 62], mouth: 'open', bow: '#4fc3f7' }, 10, 60, .92)}
  ${K({ style: 'boy', specs: true, lh: [12, 100], rh: [90, 44], mouth: 'open' }, 118, 60, .92)}
  ${robot(112, 138, 1.05)}
  ${counter('SÁNG TẠO', '#d7e3f5', '#a9c1e6')}
  ${laptop(48, 156, .95)}${boat(186, 150, 1.1)}${pcb(150, 152, .8)}
`);

/* ===== 6. Kết nối tương lai ===== */
const scene6 = () => scene(`
  ${blob('#ffc9c9', '#ffe7e7')}
  ${planet(44, 38, 12)}${rocket(176, 46, 1.2, 22)}${star(86, 26, 1.1)}${sparkle(130, 30, 1.2, '#fff')}${star(204, 96, .8, '#ffd23f', 15)}${sparkle(20, 80, 1, '#fff')}
  <ellipse cx="110" cy="200" rx="92" ry="8" fill="#000" opacity=".1"/>
  ${K({ style: 'tails', hair: HAIR.black, lh: [8, 40], rh: [92, 40], mouth: 'open' }, 2, 96, .72)}
  ${K({ style: 'boy', hair: HAIR.brown, skin: SKIN.b, goggles: true, lh: [8, 40], rh: [92, 40], mouth: 'open' }, 148, 96, .72)}
  ${K({ style: 'bun', hair: HAIR.dark, specs: true, coat: true, lh: [12, 100], rh: [94, 36], mouth: 'smile' }, 60, 58, 1.0)}
`);

/* ===== trái tim trung tâm ===== */
const heartCenter = () => `
<svg viewBox="0 0 250 340" xmlns="http://www.w3.org/2000/svg" font-family="Baloo 2">
  <defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd0e0"/><stop offset="1" stop-color="#ffb6cf"/></linearGradient></defs>
  <path d="M125 54C122 34 128 16 144 8C158 22 156 44 125 54Z" fill="#6fd078" stroke="${OL}" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M125 58C110 48 100 30 84 26C82 44 96 60 125 58Z" fill="#4fb85a" stroke="${OL}" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M125 76V50" stroke="#3f8f3f" stroke-width="4" stroke-linecap="round"/>
  <path d="M125 232C28 168 4 108 30 74C54 46 100 56 125 92C150 56 196 46 220 74C246 108 222 168 125 232Z" fill="url(#hg)" stroke="#ef8fb0" stroke-width="4" stroke-linejoin="round"/>
  <path d="M42 86Q56 66 80 72" stroke="#fff" stroke-opacity=".85" stroke-width="6" fill="none" stroke-linecap="round"/>
  <g text-anchor="middle" fill="#1d3e8f" stroke="#fff" stroke-width="5" paint-order="stroke" stroke-linejoin="round" font-weight="800">
    <text x="125" y="128" font-size="52">6</text>
    <text x="125" y="156" font-size="27">Ứng dụng</text>
    <text x="125" y="183" font-size="27">của KHTN</text>
    <text x="125" y="207" font-size="19" fill="#c8282e">trong đời sống</text>
  </g>
  <path d="M125 312C70 312 28 286 20 236C70 240 112 268 125 312Z" fill="#6fd078" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M125 312C180 312 222 286 230 236C180 240 138 268 125 312Z" fill="#59c264" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M125 312C100 290 64 268 34 246M125 312C150 290 186 268 216 246" fill="none" stroke="#2f8f3a" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M60 262Q70 268 76 278M92 282Q98 288 102 298M190 262Q180 268 174 278M158 282Q152 288 148 298" fill="none" stroke="#2f8f3a" stroke-width="2" stroke-linecap="round"/>
  ${sparkle(30, 150, 1.4, '#fff')}${sparkle(222, 120, 1.2, '#ffd23f')}
</svg>`;

/* ===== trang trí nền ===== */
const school = () => `
<svg viewBox="0 0 230 190" xmlns="http://www.w3.org/2000/svg">
  <path d="M70 18V6" stroke="${OL}" stroke-width="2.4"/><path d="M70 6H92L86 12L92 18H70Z" fill="#e63946" stroke="${OL}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M10 70L70 36L130 70Z" fill="#c75a4a" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
  <rect x="20" y="70" width="100" height="88" fill="#fff0c2" stroke="${OL}" stroke-width="2.6"/>
  <rect x="120" y="82" width="86" height="76" fill="#ffe7a3" stroke="${OL}" stroke-width="2.6"/>
  <path d="M112 82L163 56L214 82Z" fill="#c75a4a" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
  <circle cx="70" cy="56" r="11" fill="#fff" stroke="${OL}" stroke-width="2.4"/><path d="M70 49V56L75 59" stroke="${OL}" stroke-width="2" fill="none" stroke-linecap="round"/>
  ${[0, 1, 2].flatMap(r => [0, 1, 2].map(c => `<rect x="${30 + c * 30}" y="${82 + r * 24}" width="20" height="16" rx="2" fill="#8fd3ff" stroke="${OL}" stroke-width="2"/>`)).join('')}
  ${[0, 1, 2].map(c => `<rect x="${130 + c * 25}" y="96" width="17" height="14" rx="2" fill="#8fd3ff" stroke="${OL}" stroke-width="2"/>`).join('')}
  <rect x="150" y="124" width="26" height="34" rx="3" fill="#c75a4a" stroke="${OL}" stroke-width="2.4"/>
  <path d="M0 160H230" stroke="${OL}" stroke-width="2.6"/>
  <rect y="160" width="230" height="30" fill="#9ccf8a"/><path d="M0 160H230" stroke="${OL}" stroke-width="2.6"/>
  ${tree(214, 168, .9)}
</svg>`;

const bgTop = () => `
<svg viewBox="0 0 1240 360" preserveAspectRatio="xMidYMin slice" xmlns="http://www.w3.org/2000/svg">
  <g opacity=".95">${cloud(130, 80, 2.2)}${cloud(980, 60, 2.4)}${cloud(620, 24, 1.8)}${cloud(1160, 170, 1.4)}${cloud(40, 230, 1.5)}</g>
  <g>${[[20, 60], [60, 110], [30, 170], [1200, 90], [1180, 230], [1210, 300]].map(([x, y], i) => leaf(x, y, 2.2, ['#6fd078', '#8bdc8e', '#4fb85a'][i % 3], i * 35)).join('')}</g>
  <g>${[[-62,'#6fd078'],[-34,'#59c264'],[-6,'#7ad47f'],[24,'#4fb85a'],[52,'#6fd078']].map(([r,c],i)=>leaf(10+i*3,222,3.2,c,r)).join('')}
     ${[[62,'#6fd078'],[34,'#59c264'],[6,'#7ad47f'],[-24,'#4fb85a'],[-52,'#6fd078']].map(([r,c],i)=>leaf(1230-i*3,222,3.2,c,r)).join('')}</g>
</svg>`;

const flower = (x, y, s, c) => G(x, y, s, `<g fill="${c}" stroke="${OL}" stroke-width="1.8">${[0, 72, 144, 216, 288].map(a => `<ellipse cy="-8" rx="5.6" ry="8" transform="rotate(${a})"/>`).join('')}</g><circle r="5.4" fill="#ffd23f" stroke="${OL}" stroke-width="1.8"/>`);

const bgBottom = () => `
<svg viewBox="0 0 1240 300" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 150Q160 110 330 150T700 140T1050 150T1240 130V300H0Z" fill="#bfe8b0"/>
  <path d="M0 200Q200 160 420 205T820 195T1240 190V300H0Z" fill="#a5dc94"/>
  <path d="M0 250Q300 220 640 255T1240 245V300H0Z" fill="#8fd17f"/>
  ${[[60, 190, 1.3, '#ff8fb1'], [140, 230, 1.5, '#ffd23f'], [200, 205, 1, '#ffffff'], [240, 262, 1.3, '#ff8fb1'], [920, 205, 1.4, '#ffffff'], [1040, 258, 1.6, '#ff8fb1'], [1110, 210, 1.2, '#ffd23f'], [1190, 262, 1.5, '#ffffff'], [330, 215, 1.1, '#ffd23f']].map(a => flower(...a)).join('')}
  ${[[30, 240, 1.5, 20], [1215, 232, 1.6, -20], [1150, 160, 1.3, -40], [90, 160, 1.2, 30]].map(([x, y, s, r]) => leaf(x, y, s, '#4fb85a', r)).join('')}
</svg>`;

const rainbow = () => `
<svg viewBox="0 0 360 210" xmlns="http://www.w3.org/2000/svg">
  ${['#ff6b6b', '#ffa94d', '#ffe066', '#69db7c', '#4dabf7', '#9775fa'].map((c, i) => `<path d="M${14 + i * 9} 190A${166 - i * 9} ${166 - i * 9} 0 0 1 ${346 - i * 9} 190" fill="none" stroke="${c}" stroke-width="10" stroke-opacity=".85"/>`).join('')}
  ${cloud(28, 186, 1.4)}${cloud(330, 186, 1.4)}
  ${K({ style: 'tails', lh: [6, 36], rh: [94, 40], mouth: 'open' }, 30, 74, .62)}
  ${K({ style: 'boy', hair: HAIR.brown, lh: [8, 44], rh: [92, 38], mouth: 'open' }, 100, 66, .66)}
  ${K({ style: 'pony', hair: HAIR.dark, skin: SKIN.b, lh: [6, 38], rh: [90, 40], mouth: 'open' }, 172, 70, .64)}
  ${K({ style: 'boy', goggles: true, hair: HAIR.black, lh: [8, 40], rh: [94, 36], mouth: 'open' }, 244, 74, .62)}
</svg>`;

/* biểu tượng nhỏ cho dải cam kết */
const pledgeIcons = {
  health: `<svg viewBox="0 0 48 48"><path d="M24 40C6 28 6 14 15 12C20 11 23 14 24 17C25 14 28 11 33 12C42 14 42 28 24 40Z" fill="#ff6b8a" ${sw(2)}/><path d="M8 24H17L20 18L25 30L28 24H40" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  energy: `<svg viewBox="0 0 48 48"><g transform="translate(24 22) scale(1.35)">${bulb(0, 0, 1, true).replace(/<circle cx="0" cy="-6" r="26"[^>]*\/>/, '')}</g></svg>`,
  chem: `<svg viewBox="0 0 48 48"><g transform="translate(24 26) scale(1.4)">${flask(0, 0, 1, '#b388ff')}</g></svg>`,
  eco: `<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="17" fill="#4aa3e8" ${sw(2)}/><path d="M13 16Q20 8 28 15Q34 20 26 24Q20 30 14 25Q8 22 13 16Z" fill="#6cc46a"/><path d="M28 30Q36 28 38 34Q34 40 27 38Q24 34 28 30Z" fill="#6cc46a"/></svg>`,
  tech: `<svg viewBox="0 0 48 48">${gear(18, 20, 11, '#4fc3f7')}${gear(33, 33, 8, '#ffb300', 12)}</svg>`,
  future: `<svg viewBox="0 0 48 48"><g transform="translate(24 24) scale(.95) rotate(35)">${rocket(0, 0, 1)}</g></svg>`
};
