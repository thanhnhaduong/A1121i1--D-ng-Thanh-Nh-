// Xuất poster-a4.html thành ảnh khổ A4 dọc (tỉ lệ 1 : 1,414) ở hai độ phân giải:
//   1080 x 1527 px  và  2160 x 3055 px (rõ nét gấp đôi).
// Thiết kế ở 1240 x 1754 px CSS; độ nét đạt được bằng deviceScaleFactor = rộng_ra / 1240.
// Cách chạy:  NODE_PATH=$(npm root -g) node render-a4.js [tiền-tố-tên-file]
const path = require('path');
const { chromium } = require('playwright');

const W_CSS = 1240, H_CSS = 1754;
const WIDTHS = [1080, 2160];

(async () => {
  const browser = await chromium.launch();
  const prefix = path.resolve(__dirname, process.argv[2] || 'poster-a4');
  for (const W_OUT of WIDTHS) {
    const scale = W_OUT / W_CSS;
    const H_OUT = Math.round(W_OUT * Math.SQRT2);
    const page = await browser.newPage({ viewport: { width: W_CSS, height: H_CSS }, deviceScaleFactor: scale });
    page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
    await page.goto('file://' + path.join(__dirname, 'poster-a4.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    if (W_OUT === WIDTHS[0]) {
      const o = await page.evaluate(() => { const p = document.querySelector('.page'); return [p.scrollHeight, p.clientHeight]; });
      console.log('page content height / box height (css px):', o.join(' / '));
    }
    const clip = { x: 0, y: 0, width: W_CSS, height: H_OUT / scale };
    await page.screenshot({ path: `${prefix}-${W_OUT}.png`, clip });
    await page.screenshot({ path: `${prefix}-${W_OUT}.jpg`, clip, type: 'jpeg', quality: 94 });
    console.log('saved', `${prefix}-${W_OUT}.png/.jpg`, '→', W_OUT, 'x', H_OUT);
    await page.close();
  }
  await browser.close();
})();
