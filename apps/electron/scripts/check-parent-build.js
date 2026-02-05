#!/usr/bin/env node
/**
 * Check if parent iTaK project has required Python source
 * before building the Electron app
 */

const fs = require('fs');
const path = require('path');

const projectRoot = path.join(__dirname, '..', '..', '..');
const srcPath = path.join(projectRoot, 'src', 'itak');
const pyprojectPath = path.join(projectRoot, 'pyproject.toml');

console.log('Checking iTaK project structure...');

if (!fs.existsSync(pyprojectPath)) {
  console.error('❌ Error: pyproject.toml not found in parent directory');
  console.error('   Expected at:', pyprojectPath);
  process.exit(1);
}

if (!fs.existsSync(srcPath)) {
  console.error('❌ Error: src/itak directory not found in parent directory');
  console.error('   Expected at:', srcPath);
  process.exit(1);
}

console.log('✅ Parent iTaK project structure verified');
console.log('   Source directory:', srcPath);
process.exit(0);
