// Renders SVG files to PNG at their native pixel size.
// usage: node render.js jobs.json   (jobs: [{svg, png, w, h}])
const {chromium} = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({viewport: {width: j.w, height: j.h}});
    await page.setContent(`<body style="margin:0">${fs.readFileSync(j.svg, 'utf8')}</body>`);
    await page.screenshot({path: j.png, omitBackground: true, clip: {x: 0, y: 0, width: j.w, height: j.h}});
    await page.close();
  }
  await browser.close();
})();
