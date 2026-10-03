// Xuất poster.html thành ảnh PNG + JPG (độ phân giải gấp đôi, in A4/A3 vẫn nét).
// Cách chạy:  NODE_PATH=$(npm root -g) node render.js [tên-file-không-đuôi]
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1240, height: 1860 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  await page.goto('file://' + path.join(__dirname, 'poster.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const base = path.resolve(__dirname, process.argv[2] || 'poster-ung-dung-khtn');
  await page.screenshot({ path: base + '.png', fullPage: true });
  await page.screenshot({ path: base + '.jpg', fullPage: true, type: 'jpeg', quality: 92 });
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  console.log('saved', base + '.png/.jpg', '— page height (css px):', h);
  await browser.close();
})();
