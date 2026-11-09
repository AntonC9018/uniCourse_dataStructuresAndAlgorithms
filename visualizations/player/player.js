/* Course visualization player.
 *
 * Steps through traces in the unified format (see README.md): source code on the left, memory
 * with pointer arcs and struct frames above an expression-evaluation pane on the right, and the
 * program output below. Every `div.course-visualization` holding a
 * `<script type="application/json">` trace becomes a player, lazily, once its `<details>` opens.
 * Plain browser JavaScript, no dependencies; the palette lives in player.css.
 */
(() => {
  'use strict';
  if (window.CourseVisualization) return;

  // Geometry, in SVG user units --------------------------------------------------------------
  const CHAR = 0.602;                       // monospace advance, in em
  const CODE_SIZE = 25, PANE_SIZE = 30;
  const CODE_CHAR = CODE_SIZE * CHAR, EVAL_CHAR = PANE_SIZE * CHAR;
  const LINE = 56, CELL = 64, MARGIN = 28;
  const MEMORY_WIDTH = 600, MAX_BYTE = 28;
  // Struct frames hug their cells; neighbouring frames just touch.
  const FRAME = { side: 4, top: 36, bottom: 40, stroke: 2.5 };
  const GAP = 2 * FRAME.side + FRAME.stroke;
  const STACK_BELOW = 600;                  // CSS pixels: narrower players stack code above memory
  const MAX_SCALE = 0.6;                    // CSS pixels per unit: short traces do not blow up
  const DIM = 0.5;                          // opacity of variables the statement does not involve
  const T = { prepare: 0.55, travel: 1.1, settle: 0.6, follow: 0.9, writeHold: 0.8,
    copyBegin: 0.15, copyTravel: 1.0, evaluate: 0.6 };
  const KEYWORDS = new Set(['int', 'std', 'cout', 'endl', 'struct', 'auto', 'const']);
  const EASE = 'calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"';
  const PALETTE = ['bg', 'panel', 'pane', 'fg', 'muted', 'grey', 'context', 'read', 'read-fill',
    'write', 'write-fill', 'deref-fill', 'highlight', 'dead-fill', 'dead-stroke', 'gap-stroke',
    'tether'];
  const VARIABLE_COLOURS = 5, FIELD_COLOURS = 4;

  const STRINGS = {
    en: {
      play: 'Play', pause: 'Pause', back: 'Back', next: 'Next', replay: 'Replay step',
      reset: 'Reset', speed: 'Playback speed', scrub: 'Execution step', output: 'Output:',
      stage: 'Code, memory and expression evaluation', jump: 'Jump to line {line}: {code}',
      copy: 'Line {line}: {code}', read: 'Read {name}: {value}',
      addr: 'Take the address of {name}: {value}', deref: 'Follow the address in {via} to {target}',
      eval: 'Evaluate: {value}', write: 'Store {value} in {name}', print: 'Print {value}',
      error: 'This visualization could not be loaded.',
    },
    ru: {
      play: 'Пуск', pause: 'Пауза', back: 'Назад', next: 'Далее', replay: 'Повторить шаг',
      reset: 'Сначала', speed: 'Скорость', scrub: 'Шаг выполнения', output: 'Вывод:',
      stage: 'Код, память и вычисление выражения', jump: 'Перейти к строке {line}: {code}',
      copy: 'Строка {line}: {code}', read: 'Чтение {name}: {value}',
      addr: 'Адрес {name}: {value}', deref: 'Переход по адресу из {via} к {target}',
      eval: 'Вычисление: {value}', write: 'Запись {value} в {name}', print: 'Вывод {value}',
      error: 'Не удалось загрузить визуализацию.',
    },
  };
  const ICONS = {
    play: '<path d="M5 3.5v13l11-6.5z"/>',
    pause: '<path d="M5 3.5h3.5v13H5zM11.5 3.5H15v13h-3.5z"/>',
    back: '<path d="M12.5 4 6.5 10l6 6" fill="none" stroke="currentColor" stroke-width="2.2"/>',
    next: '<path d="M7.5 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2"/>',
    replay: '<path d="M15.5 10a5.5 5.5 0 1 1-1.8-4.1" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.8 2.6v4.6h-4.6z"/>',
    reset: '<path d="M4 4h2.2v12H4zM16 4v12l-8.5-6z"/>',
  };

  // Markup helpers ---------------------------------------------------------------------------
  const round = value => Math.round(value * 100) / 100;
  const esc = value => String(value).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;',
    '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]);
  const format = (template, values) => template.replace(/\{(\w+)\}/g, (_, key) => values[key] ?? '');
  // textLength pins every glyph run to the advance the layout assumes, whatever the font.
  function text(x, y, value, size, color, anchor = 'start') {
    value = String(value);
    if (!value.trim()) return '';
    const length = value.length > 1
      ? ` textLength="${round(value.length * size * CHAR)}" lengthAdjust="spacing"` : '';
    return `<text x="${round(x)}" y="${round(y)}" font-size="${size}" fill="${color}" `
      + `text-anchor="${anchor}" xml:space="preserve"${length}>${esc(value)}</text>`;
  }
  function rect(x, y, w, h, fill, stroke = 'none', radius = 8, width = 3) {
    return `<rect x="${round(x)}" y="${round(y)}" width="${round(Math.max(0, w))}" `
      + `height="${round(h)}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;
  }
  const show = at => `<set attributeName="opacity" to="1" begin="${round(at)}s" fill="freeze"/>`;
  const hide = at => `<set attributeName="opacity" to="0" begin="${round(at)}s" fill="freeze"/>`;
  const fade = (from, to, dur = 0.5, begin = 0) => `<animate attributeName="opacity" from="${from}" `
    + `to="${to}" dur="${dur}s" begin="${round(begin)}s" ${EASE} fill="freeze"/>`;
  const animateAttr = (name, from, to, dur = 0.45, begin = 0) => `<animate attributeName="${name}" `
    + `from="${typeof from === 'number' ? round(from) : from}" to="${typeof to === 'number' ? round(to) : to}" `
    + `dur="${dur}s" begin="${round(begin)}s" ${EASE} fill="freeze"/>`;
  const animated = (element, animations) => animations
    ? element.replace(/\/>$/, '>' + animations + '</' + element.match(/^<(\w+)/)[1] + '>') : element;
  const pulse = begin => `<animateTransform attributeName="transform" type="scale" values="1;1.14;1" `
    + `keyTimes="0;0.45;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" `
    + `begin="${round(begin)}s" dur="0.65s" fill="freeze"/>`;
  const markBox = (x, y, length, stroke, fill) => `<rect x="${round(x - 3)}" y="${round(y - 32)}" `
    + `width="${round(length * EVAL_CHAR + 6)}" height="42" rx="6" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
  // Starts `from` units right of its place and slides home after `begin`.
  const settle = (markup, from, begin) => from
    ? `<g transform="translate(${round(from)} 0)"><animateTransform attributeName="transform" `
      + `type="translate" from="${round(from)} 0" to="0 0" begin="${round(begin)}s" dur="0.3s" `
      + `${EASE} fill="freeze"/>${markup}</g>` : markup;
  const glide = (markup, dx, begin, dur) => dx
    ? `<g><animateTransform attributeName="transform" type="translate" from="0 0" to="${round(dx)} 0" `
      + `begin="${round(begin)}s" dur="${dur}s" ${EASE} fill="freeze"/>${markup}</g>` : markup;
  // Scales markup about a point, from `from` to `to`, during [begin, begin + dur].
  const scaleAbout = (markup, x, y, from, to, begin, dur) => `<g transform="translate(${round(x)} ${round(y)})">`
    + `<g transform="scale(${from})"><animateTransform attributeName="transform" type="scale" `
    + `from="${from}" to="${to}" begin="${round(begin)}s" dur="${dur}s" ${EASE} fill="freeze"/>`
    + `<g transform="translate(${round(-x)} ${round(-y)})">${markup}</g></g></g>`;

  // Timing -----------------------------------------------------------------------------------
  const departure = op => op.kind === 'write' ? T.writeHold : op.kind === 'print' ? 0.2 : T.prepare;
  function arrival(op) {
    if (op.kind === 'deref') return T.prepare + T.follow;
    if (op.kind === 'eval') return T.evaluate;
    if (op.kind === 'print') return 0.9;
    return departure(op) + T.travel;
  }
  const opSeconds = op => arrival(op) + T.settle + (op.kind === 'write' ? 0.5 : 0);
  const copies = (steps, i) => !steps[i].op && (i === 0 || steps[i - 1].line !== steps[i].line);
  const copyBegin = (steps, i) => i > 0 ? 0.3 : T.copyBegin;
  function animationSeconds(steps, i) {
    const step = steps[i];
    if (step.op) return opSeconds(step.op);
    return copies(steps, i) ? copyBegin(steps, i) + T.copyTravel + 0.25 : 0;
  }
  const stepSeconds = (steps, i) => steps[i].hold + animationSeconds(steps, i);

  // Model: the trace's storage flattened into cells (leaves) and struct frames (groups) --------
  function prepare(trace) {
    if (!trace || trace.format !== 1) throw new Error('unsupported trace format ' + (trace && trace.format));
    const variables = [...trace.variables].sort((a, b) => a.address - b.address);
    const leaves = [], groups = [];
    for (const variable of variables) {
      if (variable.kind !== 'struct') {
        leaves.push({ ...variable, label: variable.name, group: null });
        continue;
      }
      const fields = variable.fields.map(field => ({ name: variable.name + '.' + field.name,
        label: field.name, group: variable.name, address: variable.address + field.offset,
        size: field.size, kind: field.kind, color: variable.color, fieldColor: field.color }));
      leaves.push(...fields);
      groups.push({ name: variable.name, type: variable.type, address: variable.address,
        size: variable.size, color: variable.color, fields: fields.map(field => field.name) });
    }
    const top = variables.map(variable => variable.name);
    return { trace, steps: trace.steps, source: trace.source, spans: trace.spans || [], leaves, groups, top };
  }

  // Variables the current statement involves stay bright; the rest dim to half. A pointer's
  // target joins once evaluation reaches it.
  function activeVariables(m, i) {
    const line = m.steps[i].line, active = new Set();
    for (const token of m.source[line].match(/\b[A-Za-z_]\w*\b/g) || []) if (m.top.includes(token)) active.add(token);
    for (let j = i; j >= 0 && m.steps[j].line === line; j--) {
      for (const key of ['name', 'target', 'via']) {
        const op = m.steps[j].op;
        if (op && op[key]) active.add(op[key].split('.')[0]);
      }
    }
    return active;
  }

  // Layout -----------------------------------------------------------------------------------
  function links(g, step) {
    const list = g.leaves.filter(l => l.kind === 'ptr' && step.targets[l.name] && g.box(step.targets[l.name]))
      .map(l => ({ from: l, to: g.box(step.targets[l.name]) }));
    const centre = c => c.x + c.w / 2, ports = new Map();
    for (const l of list) {
      for (const [cell, other, key] of [[l.from, l.to, 'sx'], [l.to, l.from, 'ex']]) {
        if (!ports.has(cell.name)) ports.set(cell.name, { cell, ends: [] });
        ports.get(cell.name).ends.push({ l, key, other: centre(other) });
      }
    }
    // Ends leading left sit left of ends leading right; on each side the farther-reaching arc
    // sits nearer the centre and rises higher, so chains and shared pointees never cross.
    for (const { cell, ends } of ports.values()) {
      const side = end => end.other < centre(cell) ? 0 : 1;
      ends.sort((p, q) => side(p) - side(q) || q.other - p.other);
      const spread = 20 * (ends.length - 1);
      // Arc ends keep clear of the cell's address label.
      const low = g.isStruct(cell) ? cell.x + 12 : cell.x + 3 + labelWidth(cell) + 14, high = cell.x + cell.w - 12;
      const first = Math.min(Math.max(centre(cell) - spread / 2, low), Math.max(low, high - spread));
      ends.forEach((end, i) => { end.l[end.key] = first + i * 20; });
    }
    const range = l => [Math.min(l.sx, l.ex), Math.max(l.sx, l.ex)];
    for (const l of list) {
      const [a, b] = range(l);
      l.level = list.filter(o => o !== l && range(o)[0] >= a && range(o)[1] <= b).length;
      // An arc to a struct ends on its frame; an arc to a field passes through onto the field.
      const sy = l.from.y - 2, ey = g.isStruct(l.to) ? frameOf(l.to).y - 1 : l.to.y - 3;
      const apex = g.memY - FRAME.top - 84 - l.level * 40;
      l.d = `M ${round(l.sx)} ${sy} C ${round(l.sx)} ${apex}, ${round(l.ex)} ${apex}, ${round(l.ex)} ${ey - 9}`;
      l.head = [l.ex, ey];
    }
    return list;
  }
  const frameOf = s => ({ x: s.x - FRAME.side, y: s.y - FRAME.top, w: s.w + 2 * FRAME.side,
    h: s.h + FRAME.top + FRAME.bottom });
  const labelWidth = c => String(c.address).length * 16 * CHAR;
  const labelCentre = c => [c.x + 3 + labelWidth(c) / 2, c.y - 18];
  const valueCentre = c => [c.x + c.w / 2, c.y + 32];

  function geometry(m, P, stacked) {
    const g = { stacked, isStruct: c => Boolean(c.fields) };
    const longest = Math.max(...m.source.map(line => line.length));
    let codeW = Math.max(300, 62 + longest * CODE_CHAR + 30);
    const codeH = 44 + m.source.length * LINE;
    // Memory: top-level variables sit GAP apart, so frames hug their cells and just touch.
    const starts = [...m.groups.map(s => s.address), ...m.leaves.filter(l => !l.group).map(l => l.address)]
      .sort((a, b) => a - b);
    g.end = Math.max(...m.leaves.map(l => l.address + l.size), ...m.groups.map(s => s.address + s.size));
    g.byte = Math.min(MAX_BYTE, (MEMORY_WIDTH - GAP * (starts.length - 1)) / (g.end - starts[0]));
    const memoryW = (g.end - starts[0]) * g.byte + GAP * (starts.length - 1);
    const paneChars = Math.max(...m.steps.map(step => step.pane.length));
    const finalOutput = m.steps[m.steps.length - 1].stdout.replace(/\n$/, '');
    const outputLines = finalOutput ? finalOutput.split('\n') : [];
    const outputChars = Math.max(0, ...outputLines.map(line => line.length));
    let columnW = Math.max(360, memoryW + 48, paneChars * EVAL_CHAR + 48,
      (P.outputLabel.length + 1) * 26 * CHAR + outputChars * EVAL_CHAR + 48);
    if (stacked) codeW = columnW = Math.max(codeW, columnW);

    // The right column, from its own top: arcs, memory, names, pane, output.
    const xOf = (memX, address) => memX + (address - starts[0]) * g.byte
      + GAP * starts.filter(s => s > starts[0] && s <= address).length;
    const at = (memX, memY, c) => ({ ...c, x: xOf(memX, c.address), y: memY, w: c.size * g.byte, h: CELL });
    // Arc room comes from the highest arc any step draws.
    const probe = { ...g, memY: 0, leaves: m.leaves.map(l => at(0, 0, l)), groups: m.groups.map(s => at(0, 0, s)) };
    probe.box = name => probe.groups.find(s => s.name === name) || probe.leaves.find(l => l.name === name);
    let level = -1;
    for (const step of m.steps) for (const l of links(probe, step)) level = Math.max(level, l.level);
    const structs = m.groups.length > 0;
    const room = level >= 0 ? FRAME.top + 84 + level * 40 + 10 : (structs ? FRAME.top : 0) + 30;
    const names = structs ? CELL + FRAME.bottom + 32 : CELL + 34;
    const paneTop = room + names + 56, paneH = 76;
    const outputTop = paneTop + paneH + 60;
    const columnH = outputLines.length ? outputTop + (outputLines.length - 1) * 36 + 14 : paneTop + paneH;

    let codeX = MARGIN, codeY, columnX, columnY, width, height;
    if (stacked) {
      codeY = MARGIN;
      columnX = MARGIN;
      columnY = codeY + codeH + 24;
      width = MARGIN + columnW + 30 + MARGIN;
      height = columnY + columnH + MARGIN;
    } else {
      const content = Math.max(codeH, columnH);
      codeY = MARGIN + (content - codeH) / 2;
      columnX = codeX + codeW + 56;
      columnY = MARGIN + (content - columnH) / 2;
      width = columnX + columnW + MARGIN;
      height = MARGIN + content + MARGIN;
    }
    Object.assign(g, { width, height, code: { x: codeX, y: codeY, w: codeW, h: codeH },
      memX: columnX + 24, memY: columnY + room, pane: { x: columnX, y: columnY + paneTop, w: columnW, h: paneH },
      tx: columnX + 24, out: [columnX + 24, columnY + outputTop] });
    g.ty = g.pane.y + 38 + 11;
    g.below = g.pane.y - 56;
    g.lineY = i => g.code.y + 50 + i * LINE;
    g.xOf = address => xOf(g.memX, address);
    const colour = (list, i, count) => list[i % count];
    g.leaves = m.leaves.map(l => ({ ...at(g.memX, g.memY, l), color: colour(P.vars, l.color, VARIABLE_COLOURS),
      fieldColor: l.group ? colour(P.fields, l.fieldColor, FIELD_COLOURS) : null }));
    g.groups = m.groups.map(s => ({ ...at(g.memX, g.memY, s), color: colour(P.vars, s.color, VARIABLE_COLOURS) }));
    g.box = name => g.groups.find(s => s.name === name) || g.leaves.find(l => l.name === name);
    g.cellsOf = name => g.groups.some(s => s.name === name)
      ? g.leaves.filter(l => l.group === name) : g.leaves.filter(l => l.name === name);
    // Colouring of identifiers: variables keep their colour; a field takes its field's colour.
    g.owner = token => g.groups.find(s => s.name === token) || g.leaves.find(l => !l.group && l.name === token);
    g.field = token => g.leaves.find(l => l.group && l.label === token);
    return g;
  }

  // Scene ------------------------------------------------------------------------------------
  // `c` carries one frame's inputs: model, geometry, palette, strings, steps and focus.
  function colored(c, x, y, value, size = PANE_SIZE, mute = true, member = false) {
    let out = '';
    for (const token of value.split(/(\b[A-Za-z_]\w*\b)/)) {
      if (!token) continue;
      const owner = !member && c.g.owner(token);
      const field = !owner && c.g.field(token);
      const color = owner ? owner.color : field ? field.fieldColor
        : mute && KEYWORDS.has(token) ? c.P.context : c.P.fg;
      out += text(x, y, token, size, color);
      member = /(\.|->)$/.test(token);
      x += token.length * size * CHAR;
    }
    return out;
  }
  // pane[a, b) drawn from x; outside the evaluated span (expr) the statement is muted context.
  function paneText(c, x, y, pane, a, b, expr) {
    const member = /(\.|->)$/.test(pane.slice(0, a));
    if (!expr) return colored(c, x, y, pane.slice(a, b), PANE_SIZE, true, member);
    const cuts = [a, Math.min(b, Math.max(a, expr[0])), Math.min(b, Math.max(a, expr[1])), b];
    let out = '';
    for (let i = 0; i < 3; i++) {
      const [from, to] = [cuts[i], cuts[i + 1]];
      if (from >= to) continue;
      const px = x + (from - a) * EVAL_CHAR, part = pane.slice(from, to);
      out += i === 1 ? colored(c, px, y, part, PANE_SIZE, true, /(\.|->)$/.test(pane.slice(0, from)))
        : text(px, y, part, PANE_SIZE, c.P.context);
    }
    return out;
  }
  // The evaluated span keeps the same background as its highlight in the code.
  function exprBackground(c, x, y, expr, from = null, begin = 0) {
    if (!expr || expr[0] === expr[1]) return '';
    const box = e => [x + e[0] * EVAL_CHAR - 4, (e[1] - e[0]) * EVAL_CHAR + 8];
    const [bx, bw] = box(expr);
    let anims = '';
    if (from && from[1] > from[0] && (from[0] !== expr[0] || from[1] !== expr[1])) {
      const [fx, fw] = box(from);
      anims = animateAttr('x', fx, bx, 0.3, begin) + animateAttr('width', fw, bw, 0.3, begin);
      return animated(rect(fx, y - 33, fw, 44, c.P.highlight, 'none', 6), anims);
    }
    return rect(bx, y - 33, bw, 44, c.P.highlight, 'none', 6);
  }
  const settledPane = (c, step, x, y) => exprBackground(c, x, y, step.expr)
    + paneText(c, x, y, step.pane, 0, step.pane.length, step.expr);
  function inContext(step, span) {
    return Boolean(step.expr) && (span[1] <= step.expr[0] || span[0] >= step.expr[1]);
  }

  function dim(c, name, markup) {
    const { focus } = c, on = focus.now.has(name), was = focus.before.has(name), to = on ? 1 : DIM;
    if (on === was) return to === 1 ? markup : `<g opacity="${DIM}">${markup}</g>`;
    return `<g opacity="${was ? 1 : DIM}"><animate attributeName="opacity" from="${was ? 1 : DIM}" `
      + `to="${to}" dur="0.35s" begin="${round(focus.begin.get(name) ?? 0)}s" ${EASE} fill="freeze"/>${markup}</g>`;
  }

  function code(c, oldLine) {
    const { m, g, P, step, op } = c, x = g.code.x;
    let out = rect(x, g.code.y, g.code.w, g.code.h, P.panel);
    const box = line => {
      const source = m.source[line], span = m.spans[line] || [0, source.replace(/;\s*$/, '').length];
      return [x + 62 + span[0] * CODE_CHAR - 3, g.lineY(line) - 30, (span[1] - span[0]) * CODE_CHAR + 6];
    };
    const y = g.lineY(step.line), [bx, by, bw] = box(step.line);
    let stripe = rect(x + 8, y - 32, 4, 44, op && op.kind === 'write' ? P.write : P.read, 'none', 0);
    let span = rect(bx, by, bw, 40, P.highlight, 'none', 6);
    if (oldLine !== null) {
      const [ox, oy, ow] = box(oldLine);
      stripe = animated(stripe, animateAttr('y', g.lineY(oldLine) - 32, y - 32));
      span = animated(span, animateAttr('x', ox, bx) + animateAttr('y', oy, by) + animateAttr('width', ow, bw));
    }
    out += stripe + span;
    m.source.forEach((source, i) => {
      out += text(x + 22, g.lineY(i), i + 1, 18, P.muted)
        + colored(c, x + 62, g.lineY(i), source, CODE_SIZE, /^\s*struct\b/.test(source));
    });
    return out;
  }
  function tether(c, oldLine) {
    const { g, P, step } = c, right = g.code.x + g.code.w, mid = g.pane.y + g.pane.h / 2;
    const path = line => g.stacked
      ? `M ${round(right + 5)} ${g.lineY(line) - 10} H ${round(right + 18)} V ${mid} H ${round(g.pane.x + g.pane.w)}`
      : `M ${round(right + 5)} ${g.lineY(line) - 10} H ${round(right + 28)} V ${mid} H ${round(g.pane.x)}`;
    const d = path(step.line);
    return animated(`<path d="${d}" fill="none" stroke="${P.tether}" stroke-width="2"/>`,
      oldLine !== null ? animateAttr('d', path(oldLine), d) : '');
  }
  // Code-line controls outlive every redraw, so keyboard focus stays on them; only their
  // placement follows the geometry.
  function lineTargets(m, S) {
    return m.source.map((source, i) => `<rect class="cv-line" data-line="${i}" tabindex="0" role="button" `
      + `aria-label="${esc(format(S.jump, { line: i + 1, code: source }))}" rx="6" height="48"/>`).join('');
  }
  function placeLineTargets(g, targets) {
    targets.forEach((target, i) => {
      target.setAttribute('x', g.code.x + 12);
      target.setAttribute('y', g.lineY(i) - 34);
      target.setAttribute('width', round(g.code.w - 24));
    });
  }

  function linkMarkup(c, l, { grow = null, fadeOut = null } = {}) {
    const [x, y] = l.head, color = l.from.color;
    const head = `<path d="M -11 -6.5 L 0 0 L -11 6.5 Z" fill="${color}" transform="translate(${round(x)} ${y}) rotate(90)"/>`;
    const growing = grow !== null ? ` data-grow="${round(grow)}"` : '';
    // A background halo keeps arcs legible where they pass address labels.
    return dim(c, l.from.name.split('.')[0], `<g>`
      + (fadeOut !== null ? fade(1, 0, 0.3, fadeOut) : '')
      + `<path d="${l.d}" fill="none" stroke="${c.P.bg}" stroke-width="9"${growing}/>`
      + `<path d="${l.d}" fill="none" stroke="${color}" stroke-width="2.5"${growing}/>`
      + (grow !== null ? `<g opacity="0">${fade(0, 1, 0.15, grow + 0.5)}${head}</g>` : head) + '</g>');
  }
  function arrows(c) {
    const { g, step, prev, op } = c, now = links(g, step);
    const writesPointer = op && op.kind === 'write' && g.cellsOf(op.name).some(l => l.kind === 'ptr');
    if (writesPointer) {
      // Redirecting fades the old arc as the new address arrives, then draws the new one.
      const at = arrival(op), changed = new Set(g.cellsOf(op.name).map(l => l.name));
      let out = '';
      for (const l of links(g, prev)) out += linkMarkup(c, l, changed.has(l.from.name) ? { fadeOut: at } : {});
      for (const l of now) if (changed.has(l.from.name)) out += linkMarkup(c, l, { grow: at + 0.1 });
      return out;
    }
    let out = now.map(l => linkMarkup(c, l)).join('');
    if (op && op.kind === 'deref') {
      // The followed arc brightens from pointer to pointee.
      const l = now.find(l => l.from.name === op.via);
      if (l) out += `<path d="${l.d}" fill="none" stroke="${l.from.color}" stroke-width="7" stroke-linecap="round" data-follow="${T.prepare}"/>`;
    }
    return out;
  }
  // Highlights cover a struct's frame for struct operations and one cell for field operations.
  function outline(c, box, color) {
    if (c.g.isStruct(box)) {
      const f = frameOf(box);
      return rect(f.x + 3, f.y + 3, f.w - 6, f.h - 6, 'none', color, 8, 3);
    }
    return rect(box.x + 4.5, box.y + 4.5, box.w - 9, box.h - 9, 'none', color, 0, 3);
  }
  function memory(c) {
    const { g, P, step, prev, op } = c;
    const values = op && op.kind === 'write' ? prev.values : step.values, at = op ? arrival(op) : 0;
    const writing = new Set(op && op.kind === 'write' ? g.cellsOf(op.name).map(l => l.name) : []);
    const live = l => values[l.name] !== null || writing.has(l.name);
    let out = '';
    // Unused bytes (padding, gaps between variables) are dashed and unlabelled.
    const spans = g.leaves.map(l => [l.address, l.address + l.size]).sort((a, b) => a[0] - b[0]);
    let cursor = spans[0][0];
    for (const [a, b] of [...spans, [g.end, g.end]]) {
      if (a > cursor) out += `<rect x="${round(g.xOf(cursor) + 3)}" y="${g.memY + 3}" width="${round((a - cursor) * g.byte - 6)}" `
        + `height="58" fill="none" stroke="${P.gapStroke}" stroke-dasharray="5 5"/>`;
      cursor = Math.max(cursor, b);
    }
    for (const s of g.groups) {
      const on = g.leaves.some(l => l.group === s.name && live(l)), f = frameOf(s);
      out += dim(c, s.name, rect(f.x, f.y, f.w, f.h, 'none', on ? s.color : P.deadStroke, 6, FRAME.stroke)
        + text(s.x + s.w / 2, f.y + f.h + 32, s.name, 26, on ? s.color : P.grey, 'middle'));
    }
    if (op && op.kind === 'addr') {
      // Taking an address reads the label above storage, not the value.
      const cell = g.cellsOf(op.name)[0], [lx, ly] = labelCentre(cell);
      out += `<g opacity="0">${fade(0, 1, 0.15)}${fade(1, 0, 0.2, at + 0.1)}`
        + rect(lx - labelWidth(cell) / 2 - 5, ly - 13, labelWidth(cell) + 10, 24, P.readFill, P.read, 5, 2) + '</g>';
    }
    for (const cell of g.leaves) {
      const on = live(cell), changing = writing.has(cell.name), color = cell.fieldColor || cell.color;
      let markup = text(cell.x + 3, cell.y - 12, cell.address, 16, on ? P.muted : P.grey);
      markup += cell.group ? text(cell.x + cell.w / 2, cell.y + cell.h + 28, cell.label, 20, on ? color : P.grey, 'middle')
        : text(cell.x + cell.w / 2, cell.y + cell.h + 34, cell.label, 26, on ? color : P.grey, 'middle');
      markup += rect(cell.x, cell.y, cell.w, cell.h, on ? P.panel : P.deadFill, 'none', 0);
      markup += rect(cell.x + 1.5, cell.y + 1.5, cell.w - 3, cell.h - 3, 'none', on ? color : P.deadStroke, 0, 3);
      if (on) {
        const shown = value => {
          const length = String(value).length, size = Math.min(30, (cell.w - 12) / (length * CHAR));
          return text(0, size / 3 + 1, value, round(size), value === '?' ? P.grey : P.fg, 'middle');
        };
        markup += `<g transform="translate(${round(cell.x + cell.w / 2)} ${cell.y + cell.h / 2})"><g>` + (changing ? pulse(at - 0.2) : '');
        const before = prev ? prev.values[cell.name] : null, after = step.values[cell.name];
        // A hard cut on arrival: the old value never shows under the new one.
        if (changing && before !== after) {
          if (before !== null) markup += `<g>${hide(at)}${shown(before)}</g>`;
          markup += `<g opacity="0">${show(at)}${shown(after)}</g>`;
        } else markup += shown(changing ? after : values[cell.name]);
        markup += '</g></g>';
      }
      out += dim(c, cell.group || cell.name, markup);
    }
    if (op && (op.kind === 'read' || op.kind === 'write')) {
      out += `<g>${fade(1, 0, 0.35, at + 0.15)}${outline(c, g.box(op.name), op.kind === 'write' ? P.write : P.read)}</g>`;
    }
    // Dereference selects a location without reading it: a neutral outline.
    if (op && op.kind === 'deref') out += `<g opacity="0">${fade(0, 1, 0.2, at - 0.15)}${outline(c, g.box(op.target), P.fg)}</g>`;
    return out;
  }
  function valueBox(c, value, color, path, begin, travel, end) {
    const half = Math.max(28, String(value).length * EVAL_CHAR / 2 + 12);
    return `<g opacity="0">${fade(0, 0.55, 0.25, begin)}${fade(0.55, 0, 0.2, end - 0.2)}<path d="${path}" fill="none" stroke="${color}" stroke-width="3"/></g>`
      + `<g opacity="0">${fade(0, 1, 0.12, begin)}${hide(end)}`
      + rect(-half, -25, 2 * half, 50, c.P.panel, color, 9) + text(0, 11, value, PANE_SIZE, c.P.fg, 'middle')
      + `<animateMotion begin="${round(begin)}s" dur="${travel}s" path="${path}" keyPoints="0;1" ${EASE} fill="freeze"/></g>`;
  }
  function transfers(c) {
    const { g, P, op } = c;
    if (!op) return '';
    const at = arrival(op), begin = departure(op), ty = g.ty - 11, below = g.below;
    const spanCentre = span => g.tx + (span[0] + span[1]) / 2 * EVAL_CHAR;
    const p = (...values) => values.map(round).join(' ');
    if (op.kind === 'read') {
      const [sx, sy] = valueCentre(g.box(op.name)), dx = spanCentre(op.span);
      return valueBox(c, op.value, P.read, `M ${p(sx, sy)} C ${p(sx, below)}, ${p(dx, below)}, ${p(dx, ty)}`, begin, T.travel, at);
    }
    if (op.kind === 'addr') {
      const cell = g.cellsOf(op.name)[0], [sx, sy] = labelCentre(cell), dx = spanCentre(op.span), side = cell.x - 20;
      return valueBox(c, op.value, P.read, `M ${p(sx, sy)} C ${p(side, sy)}, ${p(side, g.memY + CELL)}, ${p(side, below)} `
        + `C ${p(side, ty)}, ${p(dx, ty - 60)}, ${p(dx, ty)}`, begin, T.travel, at);
    }
    if (op.kind === 'write') {
      const sx = spanCentre(op.span), [ex, ey] = valueCentre(g.box(op.name));
      return valueBox(c, op.value, P.write, `M ${p(sx, ty)} C ${p(sx, below)}, ${p(ex, below)}, ${p(ex, ey)}`, begin, T.travel, at);
    }
    return '';
  }
  function pane(c, copying) {
    const { g, P, step, prev, op } = c, tx = g.tx, ty = g.ty;
    let out = rect(g.pane.x, g.pane.y, g.pane.w, g.pane.h, P.pane);
    if (copying) {
      // The statement lifts off its line in an opaque box and replaces the previous one.
      const sx = g.code.x + 62, sy = g.lineY(step.line), begin = copyBegin(c.m.steps, c.index), total = begin + T.copyTravel;
      if (prev && prev.line !== step.line) out += `<g>${fade(1, 0, 0.3, begin + 0.2)}${settledPane(c, prev, tx, ty)}</g>`;
      const scale = CODE_SIZE / PANE_SIZE;
      out += `<g><animateMotion dur="${round(total)}s" path="M ${round(sx)} ${sy} L ${tx} ${ty}" keyPoints="0;0;1" `
        + `keyTimes="0;${(begin / total).toFixed(4)};1" calcMode="spline" keySplines="0 0 1 1;0.4 0 0.2 1" fill="freeze"/>`
        + `<g transform="scale(${scale})"><animateTransform attributeName="transform" type="scale" from="${scale}" to="1" `
        + `begin="${begin}s" dur="${T.copyTravel}s" ${EASE} fill="freeze"/>`
        + `<g opacity="0">${fade(0, 1, 0.15, begin - 0.15)}${fade(1, 0, 0.12, total)}`
        + rect(-8, -36, step.pane.length * EVAL_CHAR + 16, 48, P.highlight, P.read, 7, 2) + '</g>'
        + settledPane(c, step, 0, 0) + '</g></g>';
      return out;
    }
    if (op && ['read', 'addr', 'deref', 'eval'].includes(op.kind)) {
      const before = prev.pane, [s, e] = op.span, length = step.pane.length - before.length + (e - s);
      const at = arrival(op), dx = (length - (e - s)) * EVAL_CHAR, sx = tx + s * EVAL_CHAR;
      const [stroke, fill] = op.kind === 'read' || op.kind === 'addr' ? [P.read, P.readFill] : [P.fg, P.derefFill];
      out += exprBackground(c, tx, ty, step.expr, prev.expr, at + 0.1);
      out += `<g opacity="0">${fade(0, 1, 0.15)}${fade(1, 0, 0.2, at - 0.1)}${markBox(sx, ty, e - s, stroke, fill)}</g>`;
      out += paneText(c, tx, ty, before, 0, s, prev.expr);
      let old = paneText(c, sx, ty, before, s, e, prev.expr);
      let fresh = paneText(c, sx, ty, step.pane, s, s + length, step.expr);
      const middle = sx + (e - s) * EVAL_CHAR / 2;
      if (op.kind === 'eval') {
        // The operands gather into the middle of their span; the result grows out of it.
        old = scaleAbout(old, middle, ty - 11, 1, 0.45, 0.15, at - 0.15);
        fresh = scaleAbout(fresh, sx + length * EVAL_CHAR / 2, ty - 11, 0.45, 1, at, 0.25);
      }
      out += `<g>${hide(at)}${old}</g>`;
      // The new value lands centred on the token it replaces, then settles into place while
      // the rest of the line slides with it, so the two never overlap.
      out += `<g opacity="0">${show(at)}${settle(fresh, (e - s - length) / 2 * EVAL_CHAR, at + 0.1)}</g>`;
      return out + glide(paneText(c, tx + e * EVAL_CHAR, ty, before, e, before.length, prev.expr), dx, at + 0.1, 0.3);
    }
    out += exprBackground(c, tx, ty, step.expr);
    if (op && op.kind === 'write') {
      const at = arrival(op), [vs, ve] = op.span, [ns, ne] = op.destination;
      out += `<g opacity="0">${fade(0, 1, 0.15)}${fade(1, 0, 0.2, at + 0.15)}${markBox(tx + vs * EVAL_CHAR, ty, ve - vs, P.write, P.writeFill)}</g>`;
      out += `<g opacity="0">${fade(0, 1, 0.15)}${fade(1, 0, 0.3, at + 0.4)}`
        + rect(tx + ns * EVAL_CHAR - 3, ty - 32, (ne - ns) * EVAL_CHAR + 6, 42, 'none', P.write, 6, 2) + '</g>';
      out += paneText(c, tx, ty, step.pane, 0, step.pane.length, step.expr);
      // A muted destination takes its variable's colour while the value travels.
      if (inContext(step, op.destination)) {
        out += `<g opacity="0">${fade(0, 1, 0.2)}${fade(1, 0, 0.35, at + 0.15)}`
          + colored(c, tx + ns * EVAL_CHAR, ty, step.pane.slice(ns, ne)) + '</g>';
      }
      return out;
    }
    return out + paneText(c, tx, ty, step.pane, 0, step.pane.length, step.expr);
  }
  function output(c) {
    const { g, P, S, step, prev, op } = c;
    if (!step.stdout) return '';
    const [ox, oy] = g.out, label = S.output, vx = ox + (label.length + 1) * 26 * CHAR;
    const printing = op && op.kind === 'print', shown = printing ? prev.stdout : step.stdout;
    let out = (printing && !prev.stdout ? `<g opacity="0">${fade(0, 1, 0.25)}` : '<g>') + text(ox, oy, label, 26, P.muted) + '</g>';
    shown.split('\n').forEach((line, i) => { out += text(vx, oy + i * 36, line, PANE_SIZE, P.fg); });
    if (printing) {
      const lines = shown.split('\n'), x = vx + lines[lines.length - 1].length * EVAL_CHAR, y = oy + (lines.length - 1) * 36;
      const sx = g.tx + (op.span[0] + op.value.length / 2) * EVAL_CHAR, w = op.value.length * EVAL_CHAR;
      const p = (...values) => values.map(round).join(' ');
      out += valueBox(c, op.value, P.muted, `M ${p(sx, g.ty - 11)} C ${p(sx, y - 30)}, ${p(x + w / 2, g.ty + 20)}, ${p(x + w / 2, y - 11)}`, 0.2, 0.7, 0.9);
      out += `<g opacity="0">${show(0.9)}${text(x, y, op.value, PANE_SIZE, P.fg)}</g>`;
    }
    return out;
  }
  function scene(c) {
    const { step, prev, animate } = c;
    const lineChanged = animate && prev && prev.line !== step.line;
    const copying = animate && copies(c.m.steps, c.index);
    const oldLine = lineChanged ? prev.line : null;
    return code(c, oldLine) + tether(c, oldLine) + arrows(c) + memory(c) + pane(c, copying)
      + output(c) + transfers(c);
  }
  function describe(c) {
    const { m, S, step } = c, op = step.op;
    if (!op) return format(S.copy, { line: step.line + 1, code: m.source[step.line] });
    return format(S[op.kind], op);
  }

  // Player -----------------------------------------------------------------------------------
  const reducedMotion = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  const players = [];

  function themeName() {
    const theme = document.documentElement.dataset.theme;
    if (theme === 'light' || theme === 'dark') return theme;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  function strings() {
    const lang = (document.documentElement.lang || 'en').toLowerCase().split('-')[0];
    return STRINGS[lang] || STRINGS.en;
  }
  function icon(name) {
    return `<svg class="cv-icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false" fill="currentColor">${ICONS[name]}</svg>`;
  }

  class Player {
    constructor(host, trace) {
      this.host = host;
      this.m = prepare(trace);
      this.S = strings();
      this.index = 0;
      this.elapsed = 0;
      this.duration = 0;
      this.rate = 1;
      this.running = false;
      this.continuous = false;
      this.pristine = true;
      this.animated = false;
      this.frame = 0;
      this.build();
      this.theme();
      this.settle(0);
    }

    build() {
      const S = this.S, root = document.createElement('div');
      root.className = 'cv-player not-content';
      root.tabIndex = 0;
      root.setAttribute('role', 'group');
      root.setAttribute('aria-label', this.m.trace.title || S.stage);
      const button = (action, label, iconName, extra = '') => `<button type="button" class="cv-button${extra}" `
        + `data-action="${action}" aria-label="${esc(label)}" title="${esc(label)}">${icon(iconName)}`
        + `<span class="cv-label">${esc(label)}</span></button>`;
      root.innerHTML = '<div class="cv-view">'
        // The drawing is redrawn on every step and hidden from assistive technology; the
        // line controls above it are stable elements, so a redraw never discards focus.
        + `<svg class="cv-stage" role="group" aria-label="${esc(S.stage)}" xmlns="http://www.w3.org/2000/svg">`
        + `<g class="cv-scene" aria-hidden="true"></g><g class="cv-lines">${lineTargets(this.m, S)}</g></svg></div>`
        + '<div class="cv-controls"><div class="cv-transport">'
        + button('play', S.play, 'play', ' cv-primary') + button('back', S.back, 'back') + button('next', S.next, 'next')
        + button('replay', S.replay, 'replay', ' cv-icon-only')
        + `<select class="cv-speed" aria-label="${esc(S.speed)}" title="${esc(S.speed)}">`
        + [0.5, 1, 1.5, 2].map(v => `<option value="${v}"${v === 1 ? ' selected' : ''}>${v}×</option>`).join('') + '</select>'
        + button('reset', S.reset, 'reset', ' cv-reset') + '</div>'
        + `<div class="cv-progress"><input class="cv-scrub" type="range" min="0" max="${this.m.steps.length - 1}" value="0" `
        + `step="1" aria-label="${esc(S.scrub)}"><span class="cv-count"></span></div></div>`
        + '<div class="cv-status" aria-live="polite"></div>';
      this.host.append(root);
      this.root = root;
      this.svg = root.querySelector('.cv-stage');
      this.scene = root.querySelector('.cv-scene');
      this.lines = [...root.querySelectorAll('.cv-line')];
      this.playButton = root.querySelector('[data-action=play]');
      this.scrub = root.querySelector('.cv-scrub');
      this.count = root.querySelector('.cv-count');
      this.status = root.querySelector('.cv-status');
      root.querySelector('.cv-transport').addEventListener('click', event => {
        const target = event.target.closest('[data-action]');
        if (target) this[target.dataset.action]();
      });
      root.querySelector('.cv-speed').addEventListener('change', event => { this.rate = Number(event.target.value); });
      this.scrub.addEventListener('input', () => { this.pristine = false; this.settle(Number(this.scrub.value)); });
      this.svg.addEventListener('click', event => {
        const line = event.target.closest('[data-line]');
        if (line) this.line(Number(line.dataset.line));
      });
      root.addEventListener('keydown', event => this.key(event));
      this.stacked = null;
      if (window.ResizeObserver) {
        new ResizeObserver(() => { if (this.arrangement() !== this.stacked) this.refresh(); }).observe(root);
      }
    }

    key(event) {
      const target = event.target;
      if (target.closest('[data-line]') && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        this.line(Number(target.closest('[data-line]').dataset.line));
        return;
      }
      if (target.matches('input, select, textarea')) return;
      const actions = { ArrowLeft: 'back', ArrowRight: 'next', Home: 'reset', End: 'end' };
      if (actions[event.key]) {
        event.preventDefault();
        this[actions[event.key]]();
      } else if (event.key === ' ' && !target.matches('button')) {
        event.preventDefault();
        this.play();
      }
    }

    arrangement() {
      const width = this.root.clientWidth;
      return width > 0 && width < STACK_BELOW;
    }

    // Palette from player.css custom properties, so the stylesheet owns every colour.
    theme() {
      this.root.dataset.cvTheme = themeName();
      const style = getComputedStyle(this.root), read = name => style.getPropertyValue('--cv-' + name).trim();
      const P = { outputLabel: this.S.output };
      for (const name of PALETTE) P[name.replace(/-(\w)/g, (_, ch) => ch.toUpperCase())] = read(name) || '#808080';
      P.vars = Array.from({ length: VARIABLE_COLOURS }, (_, i) => read('var-' + i) || '#808080');
      P.fields = Array.from({ length: FIELD_COLOURS }, (_, i) => read('field-' + i) || '#808080');
      this.P = P;
    }

    refresh() {
      this.theme();
      this.render(this.animated);
      if (this.animated) this.seek(this.elapsed);
    }

    render(animate) {
      this.stacked = this.arrangement();
      const steps = this.m.steps, step = steps[this.index], prev = this.index ? steps[this.index - 1] : null;
      const g = geometry(this.m, this.P, this.stacked);
      const now = activeVariables(this.m, this.index);
      const before = animate && this.index ? activeVariables(this.m, this.index - 1) : now;
      const begin = new Map();
      // A dereference target lights up just before the followed arc arrives.
      if (animate && step.op && step.op.kind === 'deref') begin.set(step.op.target.split('.')[0], arrival(step.op) - 0.15);
      const c = { m: this.m, g, P: this.P, S: this.S, index: this.index, step, prev, animate,
        op: animate ? step.op : null, focus: { now, before, begin } };
      this.animated = animate;
      this.svg.setAttribute('viewBox', `0 0 ${Math.ceil(g.width)} ${Math.ceil(g.height)}`);
      this.svg.style.maxWidth = `${Math.ceil(g.width * MAX_SCALE)}px`;
      this.scene.innerHTML = `<rect width="100%" height="100%" fill="${this.P.bg}"/>` + scene(c);
      placeLineTargets(g, this.lines);
      this.finishPaths();
      this.seek(0);
      this.update(describe(c));
    }

    // Growing and followed arcs animate their dash offset over their measured length.
    finishPaths() {
      for (const path of this.scene.querySelectorAll('[data-grow],[data-follow]')) {
        const length = path.getTotalLength(), grow = path.dataset.grow !== undefined;
        const begin = Number(grow ? path.dataset.grow : path.dataset.follow), dur = grow ? 0.6 : T.follow;
        path.setAttribute('stroke-dasharray', `${length} ${length}`);
        path.setAttribute('stroke-dashoffset', length);
        const add = attributes => {
          const animation = document.createElementNS(this.svg.namespaceURI, 'animate');
          for (const [key, value] of Object.entries(attributes)) animation.setAttribute(key, value);
          path.append(animation);
        };
        add({ attributeName: 'stroke-dashoffset', from: length, to: 0, begin: begin + 's', dur: dur + 's',
          calcMode: 'spline', keyTimes: '0;1', keySplines: '0.4 0 0.2 1', fill: 'freeze' });
        if (!grow) add({ attributeName: 'opacity', from: 1, to: 0, begin: (begin + dur + 0.25) + 's', dur: '0.4s', fill: 'freeze' });
      }
    }

    seek(seconds) {
      this.svg.pauseAnimations();
      this.svg.setCurrentTime(seconds);
    }

    update(description) {
      const last = this.m.steps.length - 1;
      this.playButton.querySelector('.cv-icon').outerHTML = icon(this.running ? 'pause' : 'play');
      const label = this.running ? this.S.pause : this.S.play;
      this.playButton.querySelector('.cv-label').textContent = label;
      this.playButton.setAttribute('aria-label', label);
      this.playButton.title = label;
      for (const [action, disabled] of [['back', this.index === 0], ['next', this.index === last]]) {
        const button = this.root.querySelector(`[data-action=${action}]`);
        // A focused button that becomes disabled would drop focus to the page; the player
        // keeps it, so the arrow keys still step.
        if (disabled && document.activeElement === button) this.root.focus({ preventScroll: true });
        button.disabled = disabled;
      }
      this.scrub.value = this.index;
      this.count.textContent = `${this.index + 1} / ${last + 1}`;
      if (description !== undefined && this.status.textContent !== description) this.status.textContent = description;
    }

    // Transport. Settled steps show their end state; started steps animate from their start.
    settle(index) {
      this.stop();
      this.continuous = false;
      this.index = Math.max(0, Math.min(this.m.steps.length - 1, index));
      this.elapsed = this.duration = 0;
      this.render(false);
    }
    start(index, autoplay = false) {
      this.stop();
      this.pristine = false;
      this.continuous = autoplay;
      this.index = index;
      this.elapsed = 0;
      if (reducedMotion.matches) {
        // Cut straight to each state; autoplay still pauses on every step.
        this.duration = autoplay ? this.m.steps[index].hold + 0.6 : 0;
        this.render(false);
      } else {
        this.duration = stepSeconds(this.m.steps, index);
        this.render(true);
      }
      if (this.duration > 0) this.resume();
    }
    resume() {
      this.running = true;
      this.last = performance.now();
      this.update();
      if (!this.frame) this.frame = requestAnimationFrame(now => this.tick(now));
    }
    stop() {
      this.running = false;
      if (this.frame) cancelAnimationFrame(this.frame);
      this.frame = 0;
    }
    pause() {
      this.stop();
      this.update();
    }
    tick(now) {
      this.frame = 0;
      if (!this.running) return;
      this.elapsed = Math.min(this.duration, this.elapsed + (now - this.last) / 1000 * this.rate);
      this.last = now;
      if (this.animated) this.seek(this.elapsed);
      if (this.elapsed < this.duration) {
        this.frame = requestAnimationFrame(time => this.tick(time));
        return;
      }
      this.running = false;
      if (this.continuous && this.index < this.m.steps.length - 1) this.start(this.index + 1, true);
      else {
        this.continuous = false;
        this.render(false);
        this.elapsed = this.duration;
        this.update();
      }
    }
    get finished() { return this.elapsed >= this.duration; }

    play() {
      if (this.running) return this.pause();
      const last = this.m.steps.length - 1;
      if (this.pristine || (this.index === last && this.finished)) this.start(0, true);
      else if (this.finished) this.start(this.index + 1, true);
      else {
        this.continuous = true;
        this.resume();
      }
    }
    next() { if (this.index < this.m.steps.length - 1) this.start(this.index + 1); }
    back() { this.pristine = false; this.settle(this.index - 1); }
    replay() { this.start(this.index); }
    reset() { this.pristine = true; this.settle(0); }
    end() { this.pristine = false; this.settle(this.m.steps.length - 1); }
    // Jump to the start of a source line's execution: earlier writes and output are restored.
    line(line) {
      const index = this.m.steps.findIndex(step => step.line === line);
      if (index >= 0) {
        this.pristine = false;
        this.settle(index);
      }
    }
    // For tests and screenshots: show step `index` `seconds` into its animation, paused.
    inspect(index, seconds = null) {
      if (seconds === null) return this.settle(index);
      this.start(index);
      this.stop();
      this.continuous = false;
      if (this.animated) this.seek(seconds);
      this.elapsed = seconds;
      this.update();
    }
  }

  // Static layout: stable buttons preserve keyboard focus across theme changes.
  class Layout {
    constructor(host, trace) {
      if (trace.format !== 1 || !trace.records?.length) throw new Error('Invalid layout');
      this.host = host;
      this.root = document.createElement('div');
      this.root.className = 'cv-player cv-layout not-content';
      const ru = (document.documentElement.lang || '').startsWith('ru');
      const padding = ru ? 'Выравнивание' : 'Padding';
      this.root.innerHTML = trace.records.map((record, ri) => {
        const key = fi => `${ri}:${fi}`;
        const button = (fi, label, cls = '', description = '') => `<button type="button" class="cv-layout-target ${cls}"`
          + ` data-layout-key="${key(fi)}"${description ? ` aria-label="${esc(description)}" title="${esc(description)}"` : ''}>${label}</button>`;
        const rows = button('all', esc(`struct ${record.name}`), 'cv-layout-row')
          + record.fields.map((f, fi) => button(fi,
            esc(`${f.type} ${f.name};`) + `<small>+${f.offset} · ${f.size} B</small>`,
            `cv-layout-row cv-field-${fi % FIELD_COLOURS}`)).join('')
          + button('all', esc(`sizeof(${record.name}) = ${record.size}`), 'cv-layout-row');
        const bytes = Array.from({ length: record.size }, (_, offset) => {
          const fi = record.fields.findIndex(f => offset >= f.offset && offset < f.offset + f.size);
          const label = fi < 0 ? padding : record.fields[fi].name;
          return button(fi < 0 ? 'pad' : fi,
            `<span aria-hidden="true">${offset}</span><small>${fi < 0 ? '▧' : esc(label)}</small>`,
            `cv-byte ${fi < 0 ? 'cv-padding' : `cv-field-${fi % FIELD_COLOURS}`}`,
            `+${offset}: ${label}`);
        }).join('');
        return `<section class="cv-layout-record" data-layout-record="${ri}">`
          + `<div class="cv-layout-code">${rows}</div><div>`
          + `<p>alignof(${esc(record.name)}) = ${record.alignment}</p>`
          + `<div class="cv-layout-memory" style="--cv-slot:${record.alignment}">${bytes}</div>`
          + `<p>${esc(padding)}: ▧ · ${record.size} B</p></div></section>`;
      }).join('');
      host.append(this.root);
      this.locked = null;
      const target = event => event.target.closest('[data-layout-key]');
      this.root.addEventListener('pointerover', event => this.highlight(target(event)?.dataset.layoutKey));
      this.root.addEventListener('pointerleave', () => this.restore());
      this.root.addEventListener('focusin', event => this.highlight(target(event)?.dataset.layoutKey));
      this.root.addEventListener('focusout', () => queueMicrotask(() => this.restore()));
      this.root.addEventListener('click', event => {
        const key = target(event)?.dataset.layoutKey;
        this.locked = this.locked === key ? null : key;
        this.restore();
      });
      this.root.addEventListener('keydown', event => {
        if (event.key === 'Escape') { this.locked = null; this.highlight(null); }
      });
      this.refresh();
    }
    restore() {
      this.highlight(this.locked || (this.root.contains(document.activeElement)
        ? document.activeElement.dataset.layoutKey : null));
    }
    highlight(key) {
      const [record, field] = (key || '').split(':');
      for (const section of this.root.querySelectorAll('[data-layout-record]')) {
        section.classList.toggle('cv-layout-active', section.dataset.layoutRecord === record);
      }
      for (const element of this.root.querySelectorAll('[data-layout-key]')) {
        const [r, f] = element.dataset.layoutKey.split(':');
        element.classList.toggle('cv-linked', r === record && (field === 'all' || f === field));
      }
    }
    refresh() { this.root.dataset.cvTheme = themeName(); }
    pause() {}
  }

  // Discovery --------------------------------------------------------------------------------
  const closedAncestor = element => element.parentElement && element.parentElement.closest('details:not([open])');
  function initialize(host) {
    if (host.dataset.cvState === 'ready' || host.dataset.cvState === 'error') return;
    try {
      const data = host.querySelector('script[type="application/json"]');
      const trace = JSON.parse(data.textContent);
      const player = trace.kind === 'layout' ? new Layout(host, trace) : new Player(host, trace);
      host.dataset.cvState = 'ready';
      host.cvPlayer = player;
      players.push(player);
    } catch (error) {
      host.dataset.cvState = 'error';
      const message = document.createElement('p');
      message.className = 'cv-error';
      message.textContent = strings().error;
      host.append(message);
      console.error('course visualization:', error);
    }
  }
  function scan(root = document) {
    for (const host of root.querySelectorAll('div.course-visualization')) {
      if (!host.dataset.cvState) host.dataset.cvState = 'waiting';
      if (host.dataset.cvState === 'waiting' && !closedAncestor(host)) initialize(host);
    }
  }
  // `toggle` does not bubble, but it can be captured: open players lazily, pause closed ones.
  // A player hidden during a theme change is redrawn when it shows again.
  document.addEventListener('toggle', event => {
    const details = event.target;
    if (!(details instanceof HTMLDetailsElement)) return;
    if (!details.open) {
      for (const player of players) if (details.contains(player.host)) player.pause();
      return;
    }
    scan(details);
    for (const player of players) {
      if (player.stale && !closedAncestor(player.host)) {
        player.stale = false;
        player.refresh();
      }
    }
  }, true);
  const restyle = () => {
    for (const player of players) {
      if (closedAncestor(player.host)) player.stale = true;
      else player.refresh();
    }
  };
  new MutationObserver(restyle).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  if (window.matchMedia) window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', restyle);
  document.addEventListener('astro:page-load', () => scan());

  window.CourseVisualization = { version: 1, players, scan };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => scan());
  else scan();
})();
