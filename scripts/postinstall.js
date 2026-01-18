#!/usr/bin/env node
/**
 * iTaK npm postinstall script
 * 
 * Runs after `npm install itak` to:
 * 1. Install Python package via pip
 * 2. Launch the iTaK CLI with welcome screen
 */

const { execSync, spawn } = require('child_process');
const os = require('os');

console.log('\n' + '='.repeat(60));
console.log('  iTaK Agent Framework - Installing...');
console.log('='.repeat(60) + '\n');

// Detect Python command
function getPythonCommand() {
    const commands = ['python3', 'python', 'py'];
    for (const cmd of commands) {
        try {
            execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        } catch (e) {
            continue;
        }
    }
    return null;
}

// Install Python package
function installPythonPackage() {
    const python = getPythonCommand();

    if (!python) {
        console.log('  ⚠️  Python not found!');
        console.log('  Please install Python 3.10+ first:');
        console.log('  → https://www.python.org/downloads/\n');
        return false;
    }

    console.log(`  ✅ Found Python: ${python}`);
    console.log('  📦 Installing iTaK Python package...\n');

    try {
        // Install from PyPI (when published) or local
        execSync(`${python} -m pip install itak --quiet`, {
            stdio: 'inherit',
            timeout: 300000 // 5 minute timeout
        });
        console.log('\n  ✅ Python package installed!');
        return true;
    } catch (e) {
        console.log('  ⚠️  pip install failed, trying local install...');
        try {
            execSync(`${python} -m pip install -e . --quiet`, {
                stdio: 'inherit',
                cwd: __dirname.replace('/scripts', '').replace('\\scripts', '')
            });
            console.log('\n  ✅ Python package installed (local)!');
            return true;
        } catch (e2) {
            console.log('\n  ❌ Failed to install Python package');
            return false;
        }
    }
}

// Launch iTaK CLI
function launchCLI() {
    console.log('\n  🚀 Launching iTaK...\n');

    const python = getPythonCommand();
    if (!python) return;

    try {
        // Run the CLI
        const child = spawn(python, ['-m', 'itak.cli.cli'], {
            stdio: 'inherit',
            shell: true
        });

        child.on('error', (err) => {
            console.log(`  Note: Run 'itak' manually to start\n`);
        });
    } catch (e) {
        console.log('  Note: Run `itak` to start the iTaK Agent Framework\n');
    }
}

// Main
async function main() {
    const success = installPythonPackage();

    if (success) {
        launchCLI();
    } else {
        console.log('\n  Manual install:');
        console.log('  pip install itak');
        console.log('  itak\n');
    }
}

main();
