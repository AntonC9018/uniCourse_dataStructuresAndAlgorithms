/** Export the final state of a layout trace as a static 1280 × 720 SVG.
 * Generate layout-prototype.html first. Requires Playwright and Chromium.
 * PLAYWRIGHT_MODULE optionally selects an installed Playwright package.
 * COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE optionally selects the browser binary.
 * VISUALIZATION_INPUT and VISUALIZATION_OUTPUT override the page and the target file.
 * Usage: node visualizations/export-layout-svg.cjs [expression|swap]
 */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const fs = require('node:fs');

async function main() {
  const example = process.argv[2] || 'expression';
  if (!['expression', 'swap'].includes(example)) throw Error('Choose expression or swap');
  const target = process.env.VISUALIZATION_OUTPUT ||
    path.join(__dirname, 'renders', `layout-${example}.svg`);
  const input = process.env.VISUALIZATION_INPUT || path.join(__dirname, 'layout-prototype.html');
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE
      ? { executablePath: process.env.COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE } : {}),
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    const errors = [];
    page.on('pageerror', error => errors.push(String(error)));
    await page.goto(pathToFileURL(input).href + '?variant=B');
    const svg = await page.evaluate(selected => {
      scenario = selected;
      index = traces[scenario].steps.length - 1;
      resetLayout();
      draw();
      const stage = document.getElementById('stage');
      stage.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      stage.setAttribute('width', '1280'); stage.setAttribute('height', '720');
      const background = document.createElementNS(stage.namespaceURI, 'rect');
      for (const [key, value] of Object.entries({ width: 1280, height: 720, fill: '#101722' }))
        background.setAttribute(key, value);
      stage.prepend(background);
      return stage.outerHTML;
    }, example === 'expression' ? 0 : 1);
    if (errors.length) throw Error(errors.join('\n'));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, svg);
    console.log(target);
  } finally {
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
