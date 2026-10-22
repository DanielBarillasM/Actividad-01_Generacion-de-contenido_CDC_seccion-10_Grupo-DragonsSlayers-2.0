const slides = [...document.querySelectorAll('.slide')];
const previousButton = document.querySelector('#previous');
const nextButton = document.querySelector('#next');
const counter = document.querySelector('#counter');
const progressBar = document.querySelector('#progress-bar');
let currentSlide = 0;

function showSlide(index) {
  currentSlide = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, slideIndex) => {
    const active = slideIndex === currentSlide;
    slide.classList.toggle('is-active', active);
    slide.setAttribute('aria-hidden', String(!active));
  });
  counter.textContent = `${currentSlide + 1} / ${slides.length}`;
  progressBar.style.width = `${((currentSlide + 1) / slides.length) * 100}%`;
  document.title = `${slides[currentSlide].dataset.title} · MiniLang`;
  history.replaceState(null, '', `#${currentSlide + 1}`);
}

function isEditing() {
  return ['TEXTAREA', 'INPUT'].includes(document.activeElement?.tagName);
}

previousButton.addEventListener('click', () => showSlide(currentSlide - 1));
nextButton.addEventListener('click', () => showSlide(currentSlide + 1));
document.querySelectorAll('[data-action="next"]').forEach(button => button.addEventListener('click', () => showSlide(currentSlide + 1)));

document.addEventListener('keydown', event => {
  if (isEditing()) return;
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) {
    event.preventDefault();
    showSlide(currentSlide + 1);
  }
  if (['ArrowLeft', 'PageUp'].includes(event.key)) {
    event.preventDefault();
    showSlide(currentSlide - 1);
  }
  if (event.key === 'Home') showSlide(0);
  if (event.key === 'End') showSlide(slides.length - 1);
});

function tokenize(source) {
  const rules = [
    ['WHITESPACE', /^\s+/], ['COMMENT', /^\/\/[^\n]*/], ['NUMBER', /^\d+/],
    ['IDENTIFIER', /^[A-Za-z_][A-Za-z0-9_]*/], ['SYMBOL', /^[=+\-*/();]/]
  ];
  const keywords = new Map([['let', 'LET'], ['print', 'PRINT']]);
  const symbols = new Map([['=', 'EQUAL'], ['+', 'PLUS'], ['-', 'MINUS'], ['*', 'STAR'], ['/', 'SLASH'], ['(', 'LEFT_PAREN'], [')', 'RIGHT_PAREN'], [';', 'SEMICOLON']]);
  const tokens = [];
  let rest = source;
  while (rest.length) {
    let matched = false;
    for (const [kind, expression] of rules) {
      const match = rest.match(expression);
      if (!match) continue;
      matched = true;
      rest = rest.slice(match[0].length);
      if (kind === 'WHITESPACE' || kind === 'COMMENT') break;
      const type = kind === 'IDENTIFIER' ? (keywords.get(match[0]) || 'IDENTIFIER') : kind === 'SYMBOL' ? symbols.get(match[0]) : kind;
      tokens.push({type, lexeme: match[0]});
      break;
    }
    if (!matched) throw new Error(`Caracter inesperado: ${rest[0]}`);
  }
  tokens.push({type: 'EOF', lexeme: ''});
  return tokens;
}

function compileDemo(source) {
  const tokens = tokenize(source);
  const match = source.match(/let\s+([A-Za-z_]\w*)\s*=\s*(\d+)\s*([+\-*/])\s*(\d+)\s*;\s*print\s*\(\s*\1\s*\)\s*;/s);
  if (!match) throw new Error('La demo interactiva espera: let nombre = numero operador numero; print(nombre);');
  const [, name, leftText, operator, rightText] = match;
  const left = Number(leftText); const right = Number(rightText);
  const operations = {'+': ['i32.add', left + right], '-': ['i32.sub', left - right], '*': ['i32.mul', left * right], '/': ['i32.div_s', Math.trunc(left / right)]};
  if (operator === '/' && right === 0) throw new Error('Division por cero durante la ejecucion.');
  const [instruction, value] = operations[operator];
  const ast = {type: 'Program', statements: [{type: 'LetStatement', name, initializer: {type: 'BinaryExpression', operator, left: {type: 'NumberLiteral', value: left}, right: {type: 'NumberLiteral', value: right}}}, {type: 'PrintStatement', expression: {type: 'Identifier', name}}]};
  const wat = `(module\n  (import "env" "print_i32" (func $print_i32 (param i32)))\n  (func (export "main")\n    (local $${name} i32)\n    i32.const ${left}\n    i32.const ${right}\n    ${instruction}\n    local.set $${name}\n    local.get $${name}\n    call $print_i32\n  )\n)`;
  return {tokens: tokens.map(token => token.lexeme ? `${token.type.padEnd(14)} ${token.lexeme}` : token.type).join('\n'), ast: JSON.stringify(ast, null, 2), wat, run: `Salida del modulo WebAssembly:\n\n${value}`};
}

const sourceEditor = document.querySelector('#source');
const compilerOutput = document.querySelector('#compiler-output');
const compileButton = document.querySelector('#compile');
const tabs = [...document.querySelectorAll('[data-tab]')];
let compilation = compileDemo(sourceEditor.value);
let activeTab = 'tokens';

function renderCompilerOutput() {
  compilerOutput.textContent = compilation[activeTab];
}

compileButton.addEventListener('click', () => {
  try {
    compilation = compileDemo(sourceEditor.value);
    activeTab = 'run';
    tabs.forEach(tab => tab.setAttribute('aria-selected', String(tab.dataset.tab === activeTab)));
    renderCompilerOutput();
  } catch (error) {
    compilerOutput.textContent = `Error: ${error.message}`;
  }
});

tabs.forEach(tab => tab.addEventListener('click', () => {
  activeTab = tab.dataset.tab;
  tabs.forEach(item => item.setAttribute('aria-selected', String(item === tab)));
  renderCompilerOutput();
}));

const initial = Number(location.hash.slice(1));
showSlide(Number.isFinite(initial) && initial > 0 ? initial - 1 : 0);
renderCompilerOutput();

window.addEventListener('hashchange', () => {
  const requested = Number(location.hash.slice(1));
  if (Number.isFinite(requested) && requested > 0 && requested <= slides.length) {
    showSlide(requested - 1);
  }
});

