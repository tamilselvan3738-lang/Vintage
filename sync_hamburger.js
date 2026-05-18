const fs = require('fs');
const path = require('path');

const targetFiles = ['local pickup.html', 'audio lounge.html', 'home 2.html', 'contact.html'];

const indexPath = path.join(__dirname, 'index.html');
const indexContent = fs.readFileSync(indexPath, 'utf-8');

// Get Mobile Menu Button
const btnStartTag = '<!-- Mobile Hamburger -->';
const btnStartIdx = indexContent.indexOf(btnStartTag);
const btnEndIdx = indexContent.indexOf('</nav>', btnStartIdx);
if (btnStartIdx === -1 || btnEndIdx === -1) {
  console.log('Could not find Mobile Hamburger in index.html');
  process.exit(1);
}
const btnHTML = indexContent.substring(btnStartIdx, btnEndIdx);

// Get Mobile Drawer
const drawerStartTag = '<!-- mobile drawer -->';
const drawerStartIdx = indexContent.indexOf(drawerStartTag);
const drawerEndTag = '<!-- ==========================================================================';
const drawerEndIdx = indexContent.indexOf(drawerEndTag, drawerStartIdx);
if (drawerStartIdx === -1 || drawerEndIdx === -1) {
  console.log('Could not find Mobile Drawer in index.html');
  process.exit(1);
}
let drawerHTML = indexContent.substring(drawerStartIdx, drawerEndIdx);
drawerHTML = drawerHTML.replace(/\s+$/, '') + '\n\n\n\n';

// Get CSS
const cssStartTag = '/* MOBILE / TABLET (<= 1280px) */';
const cssStartIdx = indexContent.indexOf(cssStartTag);
const cssEndTag = '/* ==========================================================================';
const cssEndIdx = indexContent.indexOf(cssEndTag, cssStartIdx);
if (cssStartIdx === -1 || cssEndIdx === -1) {
  console.log('Could not find CSS in index.html');
  process.exit(1);
}
const cssHTML = indexContent.substring(cssStartIdx, cssEndIdx);

// Get JS
const jsStartTag = '// ---------- MOBILE DRAWER ----------';
const jsStartIdx = indexContent.indexOf(jsStartTag);
let jsHTML = '';
if (jsStartIdx !== -1) {
  const jsEndTag = '// scroll shadow effect';
  const jsEndIdx = indexContent.indexOf(jsEndTag, jsStartIdx);
  if (jsEndIdx !== -1) {
    jsHTML = indexContent.substring(jsStartIdx, jsEndIdx);
  }
} else {
  // alternative JS extraction
  // in index.html, let's extract the JS helpers for mobile drawer
  console.log("No specific mobile drawer JS comment, but let's just make sure we copy the styles correctly.");
}


for (const file of targetFiles) {
  const filePath = path.join(__dirname, file);
  if (!fs.existsSync(filePath)) {
    console.log(`Skipping ${file}, not found`);
    continue;
  }
  let content = fs.readFileSync(filePath, 'utf-8');

  // Replace Button
  const bStart = content.indexOf('<!-- Mobile Hamburger -->');
  if (bStart !== -1) {
    const bEnd = content.indexOf('</nav>', bStart);
    if (bEnd !== -1) {
      content = content.substring(0, bStart) + btnHTML + content.substring(bEnd);
    }
  }

  // Replace Drawer
  const dStart = content.indexOf('<!-- mobile drawer -->');
  if (dStart !== -1) {
    const dEnd = content.indexOf('<!-- ==========================================================================', dStart);
    if (dEnd !== -1) {
      content = content.substring(0, dStart) + drawerHTML + content.substring(dEnd);
    } else {
      const altEnd = content.indexOf('<section', dStart);
      if (altEnd !== -1) {
        content = content.substring(0, dStart) + drawerHTML + content.substring(altEnd);
      }
    }
  }

  // Ensure CSS is updated
  const cStart = content.indexOf('/* MOBILE / TABLET (<= 1280px) */');
  if (cStart !== -1) {
    let cEnd = content.indexOf('/* ==========================================================================', cStart);
    if (cEnd === -1) cEnd = content.indexOf('/* ========== UNIVERSAL RESPONSIVE BREAKPOINTS', cStart);
    if (cEnd !== -1) {
      content = content.substring(0, cStart) + cssHTML + content.substring(cEnd);
    }
  }

  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`Updated ${file}`);
}
