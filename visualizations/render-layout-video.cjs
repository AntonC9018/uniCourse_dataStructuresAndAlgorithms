/** Export a layout comparison SVG to a deterministic 1280 × 720 MP4.
 * Generate layout-prototype.html first. Requires Playwright, Chromium and ffmpeg.
 * PLAYWRIGHT_MODULE optionally selects an installed Playwright package.
 * COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE optionally selects the browser binary.
 * Usage: node visualizations/render-layout-video.cjs [expression|swap]
 *   [memory-strip|bridge|memory-band]; memory-strip (layout 2, B) is the default.
 */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const fs = require('node:fs');

async function main() {
  const example = process.argv[2] || 'expression';
  if (!['expression', 'swap'].includes(example)) throw Error('Choose expression or swap');
  const layouts={bridge:'A','memory-strip':'B','memory-band':'C'};
  const layout=process.argv[3] || 'memory-strip';
  const selectedVariant=layouts[layout];
  if(!selectedVariant) throw Error('Choose bridge, memory-strip or memory-band');
  const target = process.env.VISUALIZATION_OUTPUT ||
    path.join(__dirname, 'renders', `layout-${layout}-${example}-720p.mp4`);
  const input = process.env.VISUALIZATION_INPUT || path.join(__dirname, 'layout-prototype.html');
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
    await page.goto(pathToFileURL(input).href
      + '?variant='+selectedVariant);
    await page.evaluate(() => {
      for (const child of document.body.children) {
        if (child.id !== 'stage') child.style.display = 'none';
      }
      document.body.style.padding = '0';
      document.getElementById('stage').style.borderRadius = '0';
    });
    const steps = await page.evaluate(selected => {
      scenario = selected;
      index = 0;
      resetLayout();
      return traces[scenario].steps;
    }, example === 'expression' ? 0 : 1);
    if (process.env.VISUALIZATION_FORMAT === 'static') {
      const svg = await page.evaluate(() => {
        index = traces[scenario].steps.length - 1;
        draw();
        const stage=document.getElementById('stage');
        stage.setAttribute('xmlns','http://www.w3.org/2000/svg');
        stage.setAttribute('width','1280');stage.setAttribute('height','720');
        const background=document.createElementNS(stage.namespaceURI,'rect');
        for(const [key,value] of Object.entries({width:1280,height:720,fill:'#101722'}))
          background.setAttribute(key,value);
        stage.prepend(background);
        return stage.outerHTML;
      });
      fs.writeFileSync(target, svg);
      return;
    }
    encoder = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe',
      '-framerate', '60', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
      '-crf', '18', '-movflags', '+faststart', target], { stdio: ['pipe', 'inherit', 'inherit'] });
    const completion = once(encoder, 'close');
    const fps = 60;
    const stepDuration = await page.evaluate(() => stepAnimationSeconds);
    async function segment(seconds, step, animate, shift = false) {
      await page.evaluate(({ step, animate, shift }) => {
        index = step;
        draw(animate, shift);
        const svg = document.getElementById('stage');
        svg.pauseAnimations();
        svg.setCurrentTime(0);
      }, { step, animate, shift });
      // After all effects settle, reuse the exact final pixels for the remaining hold.
      const animationEnd=animate?seconds-0.1:stepDuration;
      let png;
      for (let frame = 0; frame < Math.ceil(seconds * fps); frame++) {
        if(!png || (frame-1)/fps<animationEnd) {
          await page.evaluate(time => document.getElementById('stage').setCurrentTime(time),
            frame / fps);
          png = await page.screenshot({ animations: 'allow' });
        }
        if (!encoder.stdin.write(png)) await once(encoder.stdin, 'drain');
      }
    }
    for (let step = 0; step < steps.length; step++) {
      if (steps[step].transfer !== null) {
        const transferDuration = await page.evaluate(
          i => transferSecondsFor(traces[scenario].steps[i]), step);
        await segment(transferDuration, step, true);
        await segment(steps[step].hold, step, false, true);
      } else {
        // Statement copies take extra time before the usual hold.
        const extra = await page.evaluate(i => copiesStatement(i) ? copySeconds : 0, step);
        await segment(steps[step].hold + extra, step, false, true);
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
