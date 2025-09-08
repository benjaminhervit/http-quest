window.addEventListener('DOMContentLoaded', () => {
  const terminalBodies = Array.from(document.querySelectorAll('.terminal__body'));
  runSequentially(terminalBodies, 0, 15); // 30ms per char; tweak speed
});

export function runSequentially(nodes, index = 0, speed = 30) {
  if (index >= nodes.length) return;
  typeHtml(nodes[index], speed, () => runSequentially(nodes, index + 1, speed));
}

export function typeHtml(el, speed = 30, done) {
  if (!el) return done && done();

  // 1) Clone to keep the original text contents per text node
  const sourceClone = el.cloneNode(true);

  // 2) Gather text nodes in *both* source and target (same traversal order)
  const srcTextNodes = [];
  const tgtTextNodes = [];
  collectTextNodes(sourceClone, srcTextNodes);
  collectTextNodes(el, tgtTextNodes);

  // Safety: mismatch means structure changed; bail gracefully
  if (srcTextNodes.length !== tgtTextNodes.length) {
    console.warn('Text node count mismatch; typing fallback to whole text.');
    const full = sourceClone.textContent || '';
    el.textContent = '';
    typeStringInto(el, full, speed, done);
    return;
  }

  // 3) Clear only the *text* of each target text node; keep elements & classes
  for (const n of tgtTextNodes) n.textContent = '';

  // Optional: prevent accidental clicks while typing
  const oldPointerEvents = el.style.pointerEvents;
  el.style.pointerEvents = 'none';

  let nodeIdx = 0;
  let charIdx = 0;

  function step() {
    if (nodeIdx >= srcTextNodes.length) {
      el.style.pointerEvents = oldPointerEvents || '';
      return done && done();
    }

    const fullText = srcTextNodes[nodeIdx].textContent || '';
    const targetNode = tgtTextNodes[nodeIdx];

    if (charIdx < fullText.length) {
      targetNode.textContent += fullText.charAt(charIdx++);
      setTimeout(step, speed);
    } else {
      nodeIdx++;
      charIdx = 0;
      setTimeout(step, speed);
    }
  }

  step();
}

// Depth-first traversal to collect TEXT_NODEs in document order
function collectTextNodes(node, out) {
  if (!node) return;
  // Ignore script/style tags completely
  if (node.nodeType === Node.ELEMENT_NODE) {
    const tag = node.tagName && node.tagName.toLowerCase();
    if (tag === 'script' || tag === 'style') return;
  }
  if (node.nodeType === Node.TEXT_NODE) {
    out.push(node);
  } else {
    for (const child of node.childNodes) collectTextNodes(child, out);
  }
}

// Fallback: type a plain string into an element
function typeStringInto(el, str, speed, done) {
  el.textContent = '';
  let i = 0;
  (function tick() {
    if (i < str.length) {
      el.textContent += str.charAt(i++);
      setTimeout(tick, speed);
    } else {
      done && done();
    }
  })();
}
