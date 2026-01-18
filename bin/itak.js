#!/usr/bin/env node
/**
 * iTaK CLI wrapper for npm
 * 
 * This allows running `itak` via npm/npx after npm install
 */

const { spawn } = require('child_process');

// Detect Python command
function getPythonCommand() {
    const commands = ['python3', 'python', 'py'];
    const { execSync } = require('child_process');

    for (const cmd of commands) {
        try {
            execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        } catch (e) {
            continue;
        }
    }
    return 'python';
}

const python = getPythonCommand();
const args = process.argv.slice(2);

// Run the Python CLI
const child = spawn(python, ['-m', 'itak.cli.cli', ...args], {
    stdio: 'inherit',
    shell: true
});

child.on('close', (code) => {
    process.exit(code);
});
