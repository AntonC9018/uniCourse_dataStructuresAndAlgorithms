// Browser tests for the site player: keyboard focus survives every redraw.
// Run from the course root (see visualizations/README.md):
//   nix develop --command npm test --prefix visualizations
// Chromium comes from $CHROMIUM_EXECUTABLE (the default shell sets it).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { after, before, beforeEach, test } from 'node:test';
import { chromium } from 'playwright';

const player = new URL('../player/', import.meta.url);
const read = name => readFileSync(new URL(name, player), 'utf8');
// Lines: int a = 5; int b = 6; int* p = &a; int** pp = &p; **pp = 7; …
const trace = read('fixtures/pointer-double.json').replace(/</g, '\\u003c');
const PAGE = `<!doctype html><html lang="en" data-theme="dark"><meta charset="utf-8">
<style>${read('player.css')}</style>
<div class="course-visualization"><script type="application/json">${trace}</script></div>
<script>${read('player.js')}</script>`;

let browser, page;
before(async () => {
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE || undefined });
});
after(() => browser?.close());
beforeEach(async () => {
  page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
  // A fake clock drives requestAnimationFrame, so animations finish on demand.
  await page.clock.install();
  await page.setContent(PAGE);
});

const index = () => page.evaluate(() => document.querySelector('.course-visualization').cvPlayer.index);
const focused = () => page.evaluate(() => {
  const active = document.activeElement, root = document.querySelector('.cv-player');
  return { inside: root.contains(active), line: active.dataset?.line ?? null,
    action: active.dataset?.action ?? null, tag: active.tagName };
});
const finishAnimation = () => page.clock.runFor(20_000);
// The first step of each source line, from the trace.
const firstStep = line => JSON.parse(read('fixtures/pointer-double.json')).steps.findIndex(s => s.line === line);

test('Enter on a code line keeps focus there and the arrow keys step', async () => {
  await page.focus('.cv-line[data-line="1"]');
  await page.keyboard.press('Enter');
  assert.equal(await index(), firstStep(1));
  assert.deepEqual(await focused(), { inside: true, line: '1', action: null, tag: 'rect' });

  await page.keyboard.press('ArrowRight');
  assert.equal(await index(), firstStep(1) + 1);
  // Mid-animation and after the closing redraw, focus is still on the line.
  await page.clock.runFor(300);
  assert.equal((await focused()).line, '1');
  await finishAnimation();
  assert.equal((await focused()).line, '1');
  await page.keyboard.press('ArrowRight');
  assert.equal(await index(), firstStep(1) + 2);
});

test('a theme change keeps focus', async () => {
  await page.focus('.cv-line[data-line="2"]');
  await page.keyboard.press(' ');
  const shown = await index();
  for (const theme of ['light', 'dark']) {
    await page.evaluate(value => { document.documentElement.dataset.theme = value; }, theme);
    await page.waitForFunction(value => document.querySelector('.cv-player').dataset.cvTheme === value, theme);
    assert.equal((await focused()).line, '2');
  }
  await page.keyboard.press('ArrowRight');
  assert.equal(await index(), shown + 1);
});

test('a theme change during an animation keeps focus', async () => {
  await page.focus('.cv-player [data-action="next"]');
  await page.keyboard.press('Enter');
  await page.clock.runFor(500);
  await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; });
  await page.waitForFunction(() => document.querySelector('.cv-player').dataset.cvTheme === 'light');
  assert.equal((await focused()).action, 'next');
  await finishAnimation();
  assert.equal((await focused()).action, 'next');
});

test('a button disabled under focus hands focus to the player', async () => {
  await page.click('.cv-player [data-action="next"]');
  await page.focus('.cv-player [data-action="back"]');
  // Back returns to the first step, which disables the focused Back button.
  await page.keyboard.press('Enter');
  assert.equal(await index(), 0);
  assert.deepEqual(await focused(), { inside: true, line: null, action: null, tag: 'DIV' });
  await page.keyboard.press('ArrowRight');
  assert.equal(await index(), 1);
});

// This fixture is emitted by the compiler/GDB tracer from lesson 05, example 26.
// Its copied pointer still points into s1, while s2.a keeps the old integer value.
test('a generated struct trace plays shallow copies in both themes', async () => {
  const generated = JSON.parse(readFileSync(new URL('fixtures/struct-generated.json', import.meta.url), 'utf8'));
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const theme of ['dark', 'light']) {
    const html = PAGE.replace(trace, JSON.stringify(generated).replace(/</g, '\\u003c'))
      .replace('data-theme="dark"', `data-theme="${theme}"`);
    await page.setContent(html);
    await page.evaluate(() => window.CourseVisualization.scan());
    await page.waitForSelector('.cv-player');
    await page.evaluate(() => {
      const player = document.querySelector('.course-visualization').cvPlayer;
      for (let step = 0; step < player.m.steps.length; step++) {
        player.settle(step);
        if (/NaN|undefined/.test(player.svg.innerHTML)) throw new Error('invalid struct geometry');
      }
      player.end();
    });
    await finishAnimation();
    const shown = await page.locator('.cv-stage').textContent();
    assert.match(shown, /s1/);
    assert.match(shown, /s2/);
    assert.equal(generated.steps.at(-1).values['s1.a'], 2);
    assert.equal(generated.steps.at(-1).values['s2.a'], 1);
    assert.equal(generated.steps.at(-1).targets['s2.pa'], 's1.a');
  }
  assert.deepEqual(errors, []);
});
