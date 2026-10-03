// Xuất poster.html thành ảnh khổ A4 dọc (tỉ lệ 1 : 1,414) ở độ phân giải cao.
//   2480 x 3508 px (A4 ở 300 dpi)  và  3720 x 5262 px (gấp 1,5 lần nữa).
// Thiết kế ở 1240 x 1754 px CSS; độ nét đạt bằng deviceScaleFactor = rộng_ra / 1240.
// Cách chạy:  NODE_PATH=$(npm root -g) node render.js [tiền-tố-tên-file]
const path = require('path');
const { chromium } = require('playwright');

const W_CSS = 1240, H_CSS = 1754;
const WIDTHS = (process.env.WIDTHS || '2480,3720').split(',').map(Number);

(async () => {
  const browser = await chromium.launch();
  const prefix = path.resolve(__dirname, process.argv[2] || 'poster-toi-gian');
  for (const W_OUT of WIDTHS) {
    const scale = W_OUT / W_CSS;
    const H_OUT = Math.round(H_CSS * scale);            // 1754 px CSS x scale → đúng khổ A4
    const page = await browser.newPage({ viewport: { width: W_CSS, height: H_CSS }, deviceScaleFactor: scale });
    page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
    await page.goto('file://' + path.join(__dirname, 'poster.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(600);
    if (W_OUT === WIDTHS[0]) {
      const o = await page.evaluate(() => {
        const pg = document.querySelector('.page');
        const sp = document.querySelector('.spacer').getBoundingClientRect().height;
        return [pg.scrollHeight, pg.clientHeight, Math.round(sp)];
      });
      console.log('content / box / free space (css px):', o.join(' / '));
    }
    const clip = { x: 0, y: 0, width: W_CSS, height: H_CSS };
    if (!process.env.JPG_ONLY || W_OUT === WIDTHS[0]) await page.screenshot({ path: `${prefix}-${W_OUT}.png`, clip });
    await page.screenshot({ path: `${prefix}-${W_OUT}.jpg`, clip, type: 'jpeg', quality: 93 });
    console.log('saved', `${prefix}-${W_OUT}`, '→', W_OUT, 'x', H_OUT);
    await page.close();
  }
  await browser.close();
})();
