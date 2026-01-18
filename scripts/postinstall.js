#!/usr/bin/env node
/**
 * iTaK npm postinstall script
 * 
 * Cross-platform auto-setup that:
 * 1. Detects OS (Windows/Mac/Linux)
 * 2. Installs WSL on Windows if needed
 * 3. Installs Docker Desktop/Engine
 * 4. Installs Ollama
 * 5. Pulls default LLM model
 * 6. Generates .env file
 * 7. Launches iTaK CLI
 */

const { execSync, spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');

const DEFAULT_MODEL = 'qwen3-vl:2b';
const PLATFORM = os.platform(); // 'win32', 'darwin', 'linux'

// Docker service ports
const DOCKER_SERVICES = [
    { name: 'chromadb', container: 'shared-chromadb', port: 8000, envVar: 'CHROMADB_URL' },
    { name: 'ollama', container: 'ollama', port: 11434, envVar: 'OLLAMA_URL' },
    { name: 'playwright', container: 'playwright', port: 3000, envVar: 'PLAYWRIGHT_URL' },
    { name: 'searxng', container: 'searxng', port: 8080, envVar: 'SEARXNG_URL' },
];

console.log('\n' + '='.repeat(60));
console.log('  iTaK Agent Framework - Cross-Platform Setup');
console.log('='.repeat(60));
console.log(`  Platform: ${PLATFORM === 'win32' ? 'Windows' : PLATFORM === 'darwin' ? 'macOS' : 'Linux'}`);
console.log('='.repeat(60) + '\n');

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function exec(cmd, options = {}) {
    try {
        return execSync(cmd, { encoding: 'utf8', stdio: 'pipe', ...options });
    } catch (e) {
        return null;
    }
}

function isAdmin() {
    if (PLATFORM === 'win32') {
        try {
            execSync('net session', { stdio: 'ignore' });
            return true;
        } catch {
            return false;
        }
    }
    return process.getuid && process.getuid() === 0;
}

function getPythonCommand() {
    const commands = ['python3', 'python', 'py'];
    for (const cmd of commands) {
        if (exec(`${cmd} --version`)) return cmd;
    }
    return null;
}

// ============================================================================
// WINDOWS-SPECIFIC FUNCTIONS
// ============================================================================

function checkWSL() {
    const result = exec('wsl --status');
    return result && result.includes('Default');
}

function installWSL() {
    console.log('  📦 WSL2 not found. Installing...\n');

    if (!isAdmin()) {
        console.log('  ⚠️  Admin privileges required to install WSL.');
        console.log('  Please run this command in an admin terminal:\n');
        console.log('    wsl --install\n');
        console.log('  Then restart your computer and run `npm install` again.\n');
        return false;
    }

    try {
        console.log('  Running: wsl --install');
        spawnSync('wsl', ['--install'], { stdio: 'inherit', shell: true });
        console.log('\n  ✅ WSL installation initiated.');
        console.log('  ⚠️  A RESTART IS REQUIRED to complete WSL setup.');
        console.log('  After restart, run `npm install` again.\n');
        return 'restart_required';
    } catch (e) {
        console.log(`  ❌ Failed to install WSL: ${e.message}`);
        return false;
    }
}

function checkDockerDesktopWindows() {
    // Check if Docker Desktop is installed
    const dockerPath = path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Docker', 'Docker', 'Docker Desktop.exe');
    const dockerPathW = path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Docker', 'Docker', 'Docker Desktop.exe');

    if (fs.existsSync(dockerPath) || fs.existsSync(dockerPathW)) {
        // Check if Docker is running
        const result = exec('docker --version');
        return result !== null;
    }
    return false;
}

function installDockerWindows() {
    console.log('  📦 Docker Desktop not found.\n');
    console.log('  Please install Docker Desktop manually:');
    console.log('  → https://www.docker.com/products/docker-desktop/\n');
    console.log('  After installing, run `npm install` again.\n');

    // Optionally open the download page
    try {
        exec('start https://www.docker.com/products/docker-desktop/');
    } catch { }

    return false;
}

function checkOllamaWindows() {
    const result = exec('ollama --version');
    return result !== null;
}

function installOllamaWindows() {
    console.log('  📦 Ollama not found.\n');
    console.log('  Please install Ollama manually:');
    console.log('  → https://ollama.ai/download\n');

    try {
        exec('start https://ollama.ai/download');
    } catch { }

    return false;
}

// ============================================================================
// MACOS-SPECIFIC FUNCTIONS
// ============================================================================

function checkBrewMac() {
    return exec('brew --version') !== null;
}

function installDockerMac() {
    if (!checkBrewMac()) {
        console.log('  📦 Docker not found. Homebrew not available.\n');
        console.log('  Please install Docker Desktop manually:');
        console.log('  → https://www.docker.com/products/docker-desktop/\n');
        return false;
    }

    console.log('  📦 Installing Docker via Homebrew...\n');
    try {
        spawnSync('brew', ['install', '--cask', 'docker'], { stdio: 'inherit', shell: true });
        console.log('\n  ✅ Docker Desktop installed!');
        console.log('  Please launch Docker Desktop and run `npm install` again.\n');
        return 'launch_required';
    } catch (e) {
        console.log(`  ❌ Failed to install Docker: ${e.message}`);
        return false;
    }
}

function installOllamaMac() {
    if (!checkBrewMac()) {
        console.log('  Please install Ollama: https://ollama.ai/download\n');
        return false;
    }

    console.log('  📦 Installing Ollama via Homebrew...\n');
    try {
        spawnSync('brew', ['install', 'ollama'], { stdio: 'inherit', shell: true });
        console.log('\n  ✅ Ollama installed!');
        return true;
    } catch (e) {
        console.log(`  ❌ Failed to install Ollama: ${e.message}`);
        return false;
    }
}

// ============================================================================
// LINUX-SPECIFIC FUNCTIONS
// ============================================================================

function installDockerLinux() {
    console.log('  📦 Installing Docker Engine...\n');

    // Try the official install script
    try {
        console.log('  Running Docker install script...');
        spawnSync('sh', ['-c', 'curl -fsSL https://get.docker.com | sh'], {
            stdio: 'inherit',
            shell: true
        });

        // Add user to docker group
        const user = process.env.USER || process.env.USERNAME;
        if (user) {
            exec(`sudo usermod -aG docker ${user}`);
            console.log(`  Added ${user} to docker group (logout/login to take effect)`);
        }

        console.log('\n  ✅ Docker installed!');
        return true;
    } catch (e) {
        console.log(`  ❌ Failed to install Docker: ${e.message}`);
        console.log('  Please install Docker manually: https://docs.docker.com/engine/install/\n');
        return false;
    }
}

function installOllamaLinux() {
    console.log('  📦 Installing Ollama...\n');
    try {
        spawnSync('sh', ['-c', 'curl -fsSL https://ollama.ai/install.sh | sh'], {
            stdio: 'inherit',
            shell: true
        });
        console.log('\n  ✅ Ollama installed!');
        return true;
    } catch (e) {
        console.log(`  ❌ Failed to install Ollama: ${e.message}`);
        return false;
    }
}

// ============================================================================
// CROSS-PLATFORM FUNCTIONS
// ============================================================================

function checkDocker() {
    const result = exec('docker --version');
    return result !== null;
}

function checkOllama() {
    const result = exec('ollama list');
    return result !== null;
}

function getRunningContainers() {
    try {
        const result = execSync('docker ps --format "{{.Names}}"', { encoding: 'utf8' });
        return result.split('\n').filter(n => n.trim());
    } catch {
        return [];
    }
}

function checkModelInstalled(model) {
    try {
        const result = exec('ollama list');
        return result && result.includes(model.split(':')[0]);
    } catch {
        return false;
    }
}

function pullModel(model) {
    console.log(`  📦 Pulling model: ${model}...`);
    console.log('     (This may take a few minutes)\n');

    try {
        spawnSync('ollama', ['pull', model], { stdio: 'inherit', shell: true });
        return true;
    } catch {
        return false;
    }
}

function generateEnvFile() {
    console.log('  📝 Generating .env file...\n');

    const projectRoot = __dirname.replace('/scripts', '').replace('\\scripts', '');
    const envPath = path.join(projectRoot, '.env');

    const running = getRunningContainers();

    let content = `# iTaK Agent Framework Environment Configuration
# Auto-generated by npm install
# Platform: ${PLATFORM}

# Default LLM Model
ITAK_DEFAULT_MODEL=${DEFAULT_MODEL}

# Docker Service URLs
`;

    for (const service of DOCKER_SERVICES) {
        const isRunning = running.some(name =>
            name.includes(service.name) || name === service.container
        );

        if (isRunning) {
            content += `${service.envVar}=http://localhost:${service.port}\n`;
            console.log(`  ✅ ${service.envVar}=http://localhost:${service.port}`);
        } else {
            content += `# ${service.envVar}=http://localhost:${service.port}  # Not running\n`;
            console.log(`  ⏭️  ${service.envVar} (not running)`);
        }
    }

    fs.writeFileSync(envPath, content);
    console.log(`\n  ✅ .env file created\n`);
}

function installPythonPackage() {
    const python = getPythonCommand();

    if (!python) {
        console.log('  ⚠️  Python not found!');
        console.log('  Please install Python 3.10+: https://www.python.org/downloads/\n');
        return false;
    }

    console.log(`  ✅ Found Python: ${python}`);
    console.log('  📦 Installing iTaK Python package...\n');

    try {
        execSync(`${python} -m pip install -e . --quiet`, {
            stdio: 'inherit',
            cwd: __dirname.replace('/scripts', '').replace('\\scripts', '')
        });
        console.log('\n  ✅ Python package installed!');
        return true;
    } catch {
        console.log('  ⚠️  Failed to install Python package');
        return false;
    }
}

function checkDockerServices() {
    console.log('  🐳 Checking Docker services...\n');

    if (!checkDocker()) {
        console.log('  ⚠️  Docker not available\n');
        return;
    }

    const running = getRunningContainers();

    for (const service of DOCKER_SERVICES) {
        const isRunning = running.some(name =>
            name.includes(service.name) || name === service.container
        );

        if (isRunning) {
            console.log(`  ✅ ${service.name}: Running`);
        } else {
            console.log(`  ⏭️  ${service.name}: Not running`);
        }
    }
    console.log();
}

function launchCLI() {
    console.log('\n  🚀 Launching iTaK...\n');
    try {
        spawnSync('itak', [], { stdio: 'inherit', shell: true });
    } catch {
        console.log('  ✅ Setup complete! Run `itak` to start.\n');
    }
}

// ============================================================================
// MAIN SETUP FLOW
// ============================================================================

async function setupWindows() {
    console.log('  🪟 Running Windows setup...\n');

    // Step 1: Check/Install WSL
    if (!checkWSL()) {
        const result = installWSL();
        if (result === 'restart_required') {
            process.exit(0);
        }
        if (!result) return false;
    } else {
        console.log('  ✅ WSL2: Installed');
    }

    // Step 2: Check/Install Docker
    if (!checkDockerDesktopWindows()) {
        const result = installDockerWindows();
        if (!result) return false;
    } else {
        console.log('  ✅ Docker Desktop: Installed');
    }

    // Step 3: Check/Install Ollama
    if (!checkOllamaWindows()) {
        installOllamaWindows();
    } else {
        console.log('  ✅ Ollama: Installed');
    }

    console.log();
    return true;
}

async function setupMac() {
    console.log('  🍎 Running macOS setup...\n');

    // Step 1: Check/Install Docker
    if (!checkDocker()) {
        const result = installDockerMac();
        if (result === 'launch_required') {
            process.exit(0);
        }
        if (!result) return false;
    } else {
        console.log('  ✅ Docker: Installed');
    }

    // Step 2: Check/Install Ollama
    if (!checkOllama()) {
        installOllamaMac();
    } else {
        console.log('  ✅ Ollama: Installed');
    }

    console.log();
    return true;
}

async function setupLinux() {
    console.log('  🐧 Running Linux setup...\n');

    // Step 1: Check/Install Docker
    if (!checkDocker()) {
        installDockerLinux();
    } else {
        console.log('  ✅ Docker: Installed');
    }

    // Step 2: Check/Install Ollama
    if (!checkOllama()) {
        installOllamaLinux();
    } else {
        console.log('  ✅ Ollama: Installed');
    }

    console.log();
    return true;
}

async function main() {
    // Step 1: Platform-specific setup
    let platformReady = false;

    if (PLATFORM === 'win32') {
        platformReady = await setupWindows();
    } else if (PLATFORM === 'darwin') {
        platformReady = await setupMac();
    } else {
        platformReady = await setupLinux();
    }

    if (!platformReady) {
        console.log('  ⚠️  Platform setup incomplete. Please install missing dependencies and retry.\n');
    }

    // Step 2: Check Docker services
    checkDockerServices();

    // Step 3: Generate .env file
    generateEnvFile();

    // Step 4: Install Python package
    const pythonOk = installPythonPackage();

    // Step 5: Pull default model
    if (pythonOk && checkOllama()) {
        if (!checkModelInstalled(DEFAULT_MODEL)) {
            console.log(`\n  📥 Model ${DEFAULT_MODEL} not found.`);
            pullModel(DEFAULT_MODEL);
        } else {
            console.log(`  ✅ Model ${DEFAULT_MODEL}: Installed`);
        }
    }

    // Step 6: Launch CLI
    if (pythonOk) {
        launchCLI();
    } else {
        console.log('\n  Manual steps:');
        console.log('  pip install -e .');
        console.log('  itak\n');
    }
}

main();
