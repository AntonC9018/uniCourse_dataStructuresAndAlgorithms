/** Export the actual variant A SVG to a deterministic 1280 × 720 MP4.
 * Generate layout-prototype.html first. Requires Playwright, Chromium and ffmpeg.
 * PLAYWRIGHT_MODULE optionally selects an installed Playwright package.
 * COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE optionally selects the browser binary.
 * Usage: node visualizations/render-layout-video.cjs [expression|swap]
 */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

async function main() {
  const example = process.argv[2] || 'expression';
  if (!['expression', 'swap'].includes(example)) throw Error('Choose expression or swap');
  const target = path.join(__dirname, 'renders', `layout-a-${example}-720p.mp4`);
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE
      ? { executablePath: process.env.COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE } : {}),
  });
  let encoder;
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    const errors = [];
    page.on('pageerror', error => errors.push(String(error)));
    // The export clock drives transitions; wall-clock callbacks must not change frames.
    await page.addInitScript(() => { window.setTimeout = () => 0; });
    await page.goto(pathToFileURL(path.join(__dirname, 'layout-prototype.html')).href
      + '?variant=A');
    await page.evaluate(() => {
      for (const child of document.body.children) {
        if (child.id !== 'stage') child.style.display = 'none';
      }
      document.body.style.padding = '0';
      document.getElementById('stage').style.borderRadius = '0';
    });
    const steps = await page.evaluate(selected => {
      scenario = selected;
      previousLayout = { key: 'A' + scenario, open: false,
        height: 48 + traces[scenario].source.length * 58,
        rows: traces[scenario].source.map((_, i) => 112 + i * 58) };
      return traces[scenario].steps;
    }, example === 'expression' ? 0 : 1);
    encoder = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe',
      '-framerate', '24', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
      '-crf', '18', '-movflags', '+faststart', target], { stdio: ['pipe', 'inherit', 'inherit'] });
    const completion = once(encoder, 'close');
    const fps = 24;
    async function segment(seconds, step, animate, shift = false) {
      await page.evaluate(({ step, animate, shift }) => {
        index = step;
        draw(animate, shift);
        const svg = document.getElementById('stage');
        svg.pauseAnimations();
        svg.setCurrentTime(0);
      }, { step, animate, shift });
      for (let frame = 0; frame < Math.ceil(seconds * fps); frame++) {
        await page.evaluate(time => document.getElementById('stage').setCurrentTime(time),
          frame / fps);
        const png = await page.screenshot({ animations: 'allow' });
        if (!encoder.stdin.write(png)) await once(encoder.stdin, 'drain');
      }
    }
    for (let step = 0; step < steps.length; step++) {
      if (steps[step].transfer !== null) {
        await segment(1, step, true);
        await segment(steps[step].hold, step, false, true);
      } else {
        await segment(steps[step].hold, step, false, true);
      }
    }
    if (errors.length) throw Error(errors.join('\n'));
    encoder.stdin.end();
    const [code] = await completion;
    if (code !== 0) throw Error(`ffmpeg exited ${code}`);
    console.log(target);
  } finally {
    if (encoder && encoder.exitCode === null) encoder.kill();
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
