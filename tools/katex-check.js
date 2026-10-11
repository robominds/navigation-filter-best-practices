// Parse every $$…$$ and $…$ expression in a Markdown file with KaTeX and report errors.
// Usage: (cd tools && npm install) && node tools/katex-check.js "Navigation Filter Best Practices 2025.md"
const katex = require('katex');
const fs = require('fs');

const src = fs.readFileSync(process.argv[2], 'utf8');
const lineOf = (i) => src.slice(0, i).split('\n').length;
let checked = 0;
let bad = 0;

function check(tex, index, displayMode) {
  checked++;
  try {
    katex.renderToString(tex, { displayMode, throwOnError: true, strict: false });
  } catch (e) {
    bad++;
    console.log(`L${lineOf(index)} ${displayMode ? 'DISPLAY' : 'INLINE'}: ${e.message.slice(0, 160)}`);
  }
}

// Display math; blank it out afterwards so inline matching does not see it.
let rest = src;
for (const m of src.matchAll(/\$\$([\s\S]*?)\$\$/g)) {
  check(m[1], m.index, true);
  rest = rest.slice(0, m.index) + ' '.repeat(m[0].length) + rest.slice(m.index + m[0].length);
}
for (const m of rest.matchAll(/(?<![\\$])\$([^$\n]+?)\$(?!\$)/g)) {
  check(m[1], m.index, false);
}

console.log(`${checked} checked ${bad} bad`);
process.exit(bad ? 1 : 0);
