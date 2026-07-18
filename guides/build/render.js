// Render a full guide HTML document to a print-ready PDF.
//   node render.js <input.html> <output.pdf> "<footer title>"
const path = require('/opt/node22/lib/node_modules/playwright');

(async () => {
  const [, , inFile, outFile, footTitle = 'Story Mode Guy'] = process.argv;
  if (!inFile || !outFile) {
    console.error('usage: node render.js <in.html> <out.pdf> "<footer>"');
    process.exit(1);
  }
  const browser = await path.chromium.launch({
    args: ['--no-sandbox', '--disable-gpu', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  const url = 'file://' + require('path').resolve(inFile);
  await page.goto(url, { waitUntil: 'networkidle' });

  const footer = `
    <div style="width:100%;font-family:'DejaVu Sans',Arial,sans-serif;font-size:7pt;
         color:#9aa2ab;padding:0 18mm;display:flex;justify-content:space-between;align-items:center;">
      <span>${footTitle.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</span>
      <span>storymodeguy.com</span>
      <span class="pageNumber"></span>
    </div>`;

  await page.pdf({
    path: outFile,
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: footer,
  });
  await browser.close();
  console.log('  rendered ' + outFile);
})().catch((e) => { console.error(e); process.exit(1); });
