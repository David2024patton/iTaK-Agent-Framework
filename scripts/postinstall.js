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

// Docker service ports (5-digit to avoid conflicts)
const API_GATEWAY_PORT = 28934;
const DOCKER_SERVICES = [
    { name: 'api-gateway', container: 'fastapi', port: API_GATEWAY_PORT, envVar: 'API_GATEWAY_URL' },
    { name: 'chromadb', container: 'chromadb', port: 29800, envVar: 'CHROMADB_URL' },
    { name: 'redis', container: 'redis', port: 63790, envVar: 'REDIS_URL' },
    { name: 'ollama', container: 'ollama', port: 11434, envVar: 'OLLAMA_URL' },
    { name: 'whisper', container: 'whisper', port: 69247, envVar: 'WHISPER_URL' },
    { name: 'playwright', container: 'playwright', port: 39281, envVar: 'PLAYWRIGHT_URL' },
    { name: 'searxng', container: 'searxng', port: 48192, envVar: 'SEARXNG_URL' },
    { name: 'crawl4ai', container: 'crawl4ai', port: 47836, envVar: 'CRAWL4AI_URL' },
    { name: 'comfyui', container: 'comfyui', port: 58127, envVar: 'COMFYUI_URL' },
    { name: 'supabase', container: 'supabase-db', port: 54321, envVar: 'SUPABASE_DB_URL' },
    { name: 'supabase-studio', container: 'supabase-studio', port: 54323, envVar: 'SUPABASE_STUDIO_URL' },
];

// Architecture detection
const ARCH = os.arch(); // 'x64', 'arm64', etc.
const IS_ARM = ARCH === 'arm64';

// Docker Desktop download URLs
const DOCKER_URLS = {
    win32: {
        x64: 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe',
        arm64: 'https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe'
    },
    darwin: {
        x64: 'https://desktop.docker.com/mac/main/amd64/Docker.dmg',
        arm64: 'https://desktop.docker.com/mac/main/arm64/Docker.dmg'
    }
};

// Ollama download URLs
const OLLAMA_URLS = {
    win32: 'https://ollama.ai/download/OllamaSetup.exe',
    darwin: 'https://ollama.ai/download/Ollama-darwin.zip'
};

console.log('\n' + '='.repeat(60));
console.log('  iTaK Agent Framework - Cross-Platform Setup');
console.log('='.repeat(60));
console.log(`  Platform: ${PLATFORM === 'win32' ? 'Windows' : PLATFORM === 'darwin' ? 'macOS' : 'Linux'}`);
console.log(`  Architecture: ${ARCH} ${IS_ARM ? '(ARM)' : '(x64)'}`);
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

// Detect NVIDIA GPU
function detectNvidiaGPU() {
    try {
        // Try nvidia-smi (works on Windows, Linux, macOS with NVIDIA)
        const result = exec('nvidia-smi --query-gpu=name,memory.total --format=csv,noheader');
        if (result) {
            const gpuInfo = result.trim().split('\n')[0];
            return { detected: true, info: gpuInfo.trim() };
        }
    } catch (e) { }
    return { detected: false, info: null };
}

// Download a file from URL
function downloadFile(url, destPath) {
    return new Promise((resolve, reject) => {
        console.log(`  ⬇️  Downloading from ${url.split('/').pop().split('?')[0]}...`);

        const file = fs.createWriteStream(destPath);

        const request = (url.startsWith('https') ? require('https') : require('http'))
            .get(url, { headers: { 'User-Agent': 'iTaK-Installer' } }, (response) => {
                // Handle redirects
                if (response.statusCode === 301 || response.statusCode === 302) {
                    file.close();
                    fs.unlinkSync(destPath);
                    downloadFile(response.headers.location, destPath).then(resolve).catch(reject);
                    return;
                }

                const totalSize = parseInt(response.headers['content-length'], 10);
                let downloadedSize = 0;

                response.on('data', (chunk) => {
                    downloadedSize += chunk.length;
                    if (totalSize) {
                        const percent = Math.round((downloadedSize / totalSize) * 100);
                        process.stdout.write(`\r  ⬇️  Downloading... ${percent}%   `);
                    }
                });

                response.pipe(file);

                file.on('finish', () => {
                    file.close();
                    console.log('\n  ✅ Download complete!');
                    resolve(destPath);
                });
            });

        request.on('error', (err) => {
            fs.unlink(destPath, () => { });
            reject(err);
        });
    });
}

// Download and run an installer
async function downloadAndRunInstaller(url, filename, args = []) {
    const tempDir = os.tmpdir();
    const installerPath = path.join(tempDir, filename);

    try {
        await downloadFile(url, installerPath);

        console.log(`  🚀 Running installer (you may need to approve admin access)...`);

        if (PLATFORM === 'win32') {
            // Run Windows installer
            spawnSync(installerPath, args, {
                stdio: 'inherit',
                shell: true,
                windowsHide: false
            });
        } else if (PLATFORM === 'darwin') {
            if (filename.endsWith('.dmg')) {
                // Mount DMG and run installer
                console.log('  📦 Mounting DMG...');
                exec(`hdiutil attach "${installerPath}" -nobrowse`);
                console.log('  📦 Installing Docker.app...');
                exec('cp -R "/Volumes/Docker/Docker.app" /Applications/');
                exec('hdiutil detach "/Volumes/Docker"');
            } else if (filename.endsWith('.zip')) {
                // Unzip and install
                exec(`unzip -o "${installerPath}" -d /Applications/`);
            }
        }

        // Clean up
        try { fs.unlinkSync(installerPath); } catch { }

        return true;
    } catch (e) {
        console.log(`  ❌ Installation failed: ${e.message}`);
        return false;
    }
}

// ============================================================================
// WINDOWS-SPECIFIC FUNCTIONS
// ============================================================================

function checkWSL() {
    // Method 1: Check if wsl.exe exists and runs
    try {
        // Use --status which is more reliable than -l -v (avoids UTF-16 encoding issues)
        const result = execSync('wsl --status 2>&1', { encoding: 'utf8', stdio: 'pipe', timeout: 5000 });
        // If it returns anything without error, WSL is installed
        if (result && !result.includes('not recognized')) {
            return true;
        }
    } catch (e) {
        // --status might fail even if WSL is installed (permission issues)
    }

    // Method 2: Check if wsl command exists at all
    try {
        execSync('where wsl', { encoding: 'utf8', stdio: 'pipe' });
        return true; // If 'where wsl' succeeds, WSL is installed
    } catch {
        // wsl not found in PATH
    }

    // Method 3: Check PowerShell for WSL feature
    try {
        const result = execSync('powershell -Command "Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux | Select-Object -ExpandProperty State"',
            { encoding: 'utf8', stdio: 'pipe', timeout: 10000 });
        if (result && result.includes('Enabled')) {
            return true;
        }
    } catch {
        // PowerShell check failed
    }

    return false;
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
    // Simply check if Docker CLI works
    const result = exec('docker --version');
    return result !== null;
}

async function installDockerWindows() {
    console.log('  📦 Docker Desktop not found. Installing...\n');

    const archKey = IS_ARM ? 'arm64' : 'x64';
    const url = DOCKER_URLS.win32[archKey];
    const filename = 'DockerDesktopInstaller.exe';

    console.log(`  Downloading Docker Desktop for Windows (${archKey})...`);

    const success = await downloadAndRunInstaller(url, filename, ['install', '--quiet']);

    if (success) {
        console.log('\n  ✅ Docker Desktop installed!');
        console.log('  Please start Docker Desktop and run `npm install` again.\n');
        return 'launch_required';
    }

    return false;
}

function checkOllamaWindows() {
    const result = exec('ollama --version');
    return result !== null;
}

async function installOllamaWindows() {
    console.log('  📦 Ollama not found. Installing...\n');

    const url = OLLAMA_URLS.win32;
    const filename = 'OllamaSetup.exe';

    const success = await downloadAndRunInstaller(url, filename, ['/SILENT']);

    if (success) {
        console.log('\n  ✅ Ollama installed!');
        return true;
    }

    return false;
}

// ============================================================================
// MACOS-SPECIFIC FUNCTIONS
// ============================================================================

function checkBrewMac() {
    return exec('brew --version') !== null;
}

async function installDockerMac() {
    console.log('  📦 Docker Desktop not found. Installing...\n');

    const archKey = IS_ARM ? 'arm64' : 'x64';
    const url = DOCKER_URLS.darwin[archKey];
    const filename = 'Docker.dmg';

    console.log(`  Downloading Docker Desktop for macOS (${IS_ARM ? 'Apple Silicon' : 'Intel'})...`);

    const success = await downloadAndRunInstaller(url, filename);

    if (success) {
        console.log('\n  ✅ Docker Desktop installed!');
        console.log('  Please launch Docker Desktop from Applications.\n');
        // Try to launch Docker
        exec('open /Applications/Docker.app');
        return 'launch_required';
    }

    // Fallback to Homebrew
    if (checkBrewMac()) {
        console.log('  Trying Homebrew instead...');
        try {
            spawnSync('brew', ['install', '--cask', 'docker'], { stdio: 'inherit', shell: true });
            return 'launch_required';
        } catch { }
    }

    return false;
}

async function installOllamaMac() {
    console.log('  📦 Ollama not found. Installing...\n');

    // Try Homebrew first (preferred)
    if (checkBrewMac()) {
        console.log('  Installing via Homebrew...');
        try {
            spawnSync('brew', ['install', 'ollama'], { stdio: 'inherit', shell: true });
            console.log('\n  ✅ Ollama installed!');
            return true;
        } catch { }
    }

    // Fallback to download
    const url = OLLAMA_URLS.darwin;
    const filename = 'Ollama-darwin.zip';

    const success = await downloadAndRunInstaller(url, filename);

    if (success) {
        console.log('\n  ✅ Ollama installed!');
        return true;
    }

    return false;
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

function isDockerRunning() {
    const result = exec('docker info');
    return result !== null;
}

async function waitForDocker(maxWaitSeconds = 60) {
    console.log('  ⏳ Waiting for Docker to start...');

    const startTime = Date.now();
    const maxWaitMs = maxWaitSeconds * 1000;

    while (Date.now() - startTime < maxWaitMs) {
        if (isDockerRunning()) {
            console.log('  ✅ Docker is running!');
            return true;
        }

        // Wait 3 seconds before checking again
        await new Promise(resolve => setTimeout(resolve, 3000));
        process.stdout.write('.');
    }

    console.log('\n  ⚠️  Docker is not running. Please start Docker Desktop.');
    return false;
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

// Container configurations - auto-installed during setup
const CONTAINER_CONFIGS = {
    chromadb: {
        name: 'chromadb',
        image: 'chromadb/chroma',
        ports: '29800:8000',
        required: true
    },
    ollama: {
        name: 'ollama',
        image: 'ollama/ollama',
        ports: '11434:11434',
        required: true,
        volumes: PLATFORM === 'win32' ? 'ollama:/root/.ollama' : `${os.homedir()}/.ollama:/root/.ollama`
    },
    playwright: {
        name: 'playwright',
        image: 'mcr.microsoft.com/playwright:v1.40.0-jammy',
        ports: '39281:39281',
        required: false,
        command: 'npx -y playwright@1.40.0 run-server --port 39281'
    },
    searxng: {
        name: 'searxng',
        image: 'searxng/searxng:latest',
        ports: '48192:8080',
        required: false,
        env: ['SEARXNG_BASE_URL=http://localhost:48192/']
    }
};

async function setupDockerContainers() {
    console.log('  🐳 Setting up Docker containers (api-gateway)...\n');

    if (!isDockerRunning()) {
        console.log('  ⚠️  Docker is not running. Cannot setup containers.\n');
        return false;
    }

    // Check if CORE containers are already running (skip optional ones)
    const running = getRunningContainers();
    const coreContainers = ['ollama', 'chromadb', 'searxng'];
    const coreRunning = coreContainers.filter(name =>
        running.some(r => r.includes(name) || r === name)
    );

    // If all core containers are running, skip docker compose entirely
    if (coreRunning.length === coreContainers.length) {
        console.log('  ✅ Core containers already running:');
        for (const name of coreRunning) {
            console.log(`     ✅ ${name}`);
        }
        console.log();
        return true;
    }

    // Show which containers are already running (if any)
    if (coreRunning.length > 0) {
        console.log('  ℹ️  Some containers already running:');
        for (const name of coreRunning) {
            console.log(`     ✅ ${name}`);
        }
        console.log();
    }

    // Use docker-compose from the api-gateway directory
    const projectRoot = path.resolve(__dirname, '..');
    const composeFile = path.join(projectRoot, 'docker', 'api-gateway', 'docker-compose.yml');

    console.log(`  📦 Starting api-gateway stack...`);
    console.log(`     (ollama, chromadb, searxng)\n`);

    if (fs.existsSync(composeFile)) {
        try {
            // Docker Compose up -d will:
            // - Start new containers that don't exist
            // - Leave existing containers with data untouched
            // - Only recreate if config changed (preserves volumes)
            // Use stdio: 'pipe' to capture and filter error output
            const result = spawnSync('docker', ['compose', '-f', composeFile, '-p', 'api-gateway', 'up', '-d'], {
                stdio: 'pipe',
                shell: true,
                cwd: path.dirname(composeFile),
                encoding: 'utf8'
            });

            // Check for conflicts in stderr but don't show the raw red errors
            if (result.stderr && result.stderr.includes('Conflict')) {
                console.log('  ℹ️  Containers exist outside api-gateway project.');
                console.log('     Using existing containers (this is fine!).\n');
            } else if (result.status === 0) {
                console.log('  ✅ api-gateway stack started!');
                console.log('  📦 Containers grouped under: api-gateway\n');

                // Auto-start FRP tunnel if frpc.toml exists
                const frpcConfig = path.join(path.dirname(composeFile), 'frpc.toml');
                if (fs.existsSync(frpcConfig)) {
                    console.log('  🔗 Found frpc.toml - auto-starting VPS tunnel...');
                    const tunnelResult = spawnSync('docker', ['compose', '-f', composeFile, '-p', 'api-gateway', '--profile', 'tunnel', 'up', '-d', 'frpc'], {
                        stdio: 'pipe',
                        shell: true,
                        cwd: path.dirname(composeFile)
                    });
                    if (tunnelResult.status === 0) {
                        console.log('  ✅ FRP tunnel connected to VPS!\n');
                    } else {
                        console.log('  ⚠️  FRP tunnel failed to start\n');
                    }
                }
            }

            return true;
        } catch (e) {
            console.log(`  ⚠️  Docker compose failed, using standalone containers...\n`);
        }
    }

    // Fallback to individual containers (only if compose fails)
    console.log('  ⚠️  Using standalone containers (not grouped)...\n');
    for (const [serviceName, config] of Object.entries(CONTAINER_CONFIGS)) {
        const isRunning = running.some(name =>
            name === config.name || name.includes(serviceName)
        );

        if (isRunning) {
            console.log(`  ✅ ${serviceName}: Already running`);
            continue;
        }

        console.log(`  📦 Starting ${serviceName}...`);
        let dockerCmd = `docker run -d --name ${config.name} -p ${config.ports}`;
        if (config.volumes) dockerCmd += ` -v ${config.volumes}`;
        if (config.env) {
            for (const e of config.env) dockerCmd += ` -e ${e}`;
        }
        dockerCmd += ` ${config.image}`;
        if (config.command) dockerCmd += ` ${config.command}`;

        try {
            exec(dockerCmd);
            console.log(`  ✅ ${serviceName}: Started`);
        } catch (e) {
            console.log(`  ⚠️  ${serviceName}: Failed to start`);
        }
    }
    return true;
}

function generateEnvFile() {
    console.log('  📝 Generating .env file...\n');

    const projectRoot = path.resolve(__dirname, '..');
    const envPath = path.join(projectRoot, '.env');

    const running = getRunningContainers();

    // Check for existing FRP_AUTH_TOKEN in .env - preserve it if exists!
    const crypto = require('crypto');
    let autoToken = crypto.randomBytes(16).toString('hex');
    let tokenPreserved = false;

    if (fs.existsSync(envPath)) {
        const existingEnv = fs.readFileSync(envPath, 'utf8');
        const tokenMatch = existingEnv.match(/^FRP_AUTH_TOKEN=(.+)$/m);
        if (tokenMatch && tokenMatch[1] && !tokenMatch[1].startsWith('#')) {
            autoToken = tokenMatch[1].trim();
            tokenPreserved = true;
        }
    }

    // Detect GPU
    const gpu = detectNvidiaGPU();

    let content = `# ██ ████████  ▄█████▄  ██   ██
# ██    ██    ██     ██ ██  ██ 
# ██    ██    █████████ █████  
# ██    ██    ██     ██ ██  ██ 
# ██    ██    ██     ██ ██   ██
#
# iTaK Agent Framework - Environment Configuration
# Made with ❤️ by David Patton

# Default LLM Model
ITAK_DEFAULT_MODEL=${DEFAULT_MODEL}
`;

    // Add GPU info if detected
    if (gpu.detected) {
        content += `
# ═══════════════════════════════════════════════════════════════════
# 🎮 GPU DETECTED - CUDA ACCELERATION ENABLED
# ═══════════════════════════════════════════════════════════════════
# GPU: ${gpu.info}
# Ollama will automatically use your GPU for faster inference!
`;
        console.log(`  🎮 GPU Detected: ${gpu.info}`);
    }

    content += `
# ═══════════════════════════════════════════════════════════════════
# LOCAL SERVICE URLs
# ═══════════════════════════════════════════════════════════════════
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

    // Add OpenAI-compatible IDE integration section
    content += `
# ═══════════════════════════════════════════════════════════════════
# 🔌 USE IN YOUR IDE (OpenAI-Compatible)
# ═══════════════════════════════════════════════════════════════════
#
# Your local Ollama is OpenAI-compatible! Use these settings in any IDE:
#
#   Base URL:   http://localhost:11434/v1
#   API Key:    ollama (or any string - not validated)
#   Model:      ${DEFAULT_MODEL}
#
# ┌──────────────────────────────────────────────────────────────────┐
# │ EXAMPLE: VS Code / Cursor / Continue.dev Settings               │
# ├──────────────────────────────────────────────────────────────────┤
# │ {                                                                │
# │   "openai.baseUrl": "http://localhost:11434/v1",                 │
# │   "openai.apiKey": "ollama",                                     │
# │   "openai.model": "${DEFAULT_MODEL}"                             │
# │ }                                                                │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │ EXAMPLE: cURL Test                                               │
# ├──────────────────────────────────────────────────────────────────┤
# │ curl http://localhost:11434/v1/chat/completions \\                │
# │   -H "Content-Type: application/json" \\                          │
# │   -d '{"model":"${DEFAULT_MODEL}","messages":[{"role":"user",    │
# │        "content":"Hello!"}]}'                                    │
# └──────────────────────────────────────────────────────────────────┘
#
# Works with: VS Code, Cursor, JetBrains AI, Neovim, Emacs, any OpenAI client!
# ═══════════════════════════════════════════════════════════════════
`;
    // Add VPS/FRP configuration section with auto-generated token
    content += `
# ═══════════════════════════════════════════════════════════════════
# VPS REMOTE ACCESS
# ═══════════════════════════════════════════════════════════════════
# 
# A random auth token was auto-generated for you below.
# Use this SAME token on your VPS (frps.toml) and it will auto-connect!
#
# To generate a new token manually: openssl rand -hex 16
# See docs/VPS_SETUP.md for full VPS setup instructions.
# ═══════════════════════════════════════════════════════════════════

# VPS_IP=your.vps.ip.address
FRP_AUTH_TOKEN=${autoToken}
`;

    if (tokenPreserved) {
        console.log(`\n  🔑 Preserved existing FRP_AUTH_TOKEN from .env`);
    } else {
        console.log(`\n  🔑 Auto-generated FRP_AUTH_TOKEN for VPS tunneling`);
        console.log(`     Use this token in your VPS frps.toml auth.token setting`);
    }

    fs.writeFileSync(envPath, content);
    console.log(`  ✅ .env file created\n`);
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

function installAgentBrowser() {
    console.log('  🌐 Installing Agent Browser CLI...\n');

    try {
        // Check if already installed
        const result = execSync('agent-browser --version 2>&1', { encoding: 'utf8', stdio: 'pipe' });
        console.log(`  ✅ Agent Browser already installed: ${result.trim()}`);
        return true;
    } catch {
        // Not installed, install it
    }

    try {
        console.log('  📦 Installing @anthropic-ai/agent-browser globally...');
        execSync('npm install -g @anthropic-ai/agent-browser', { stdio: 'inherit' });

        // On Linux/WSL, install playwright deps
        if (PLATFORM === 'linux') {
            console.log('  📦 Installing Playwright dependencies for Linux...');
            try {
                execSync('npx playwright install-deps', { stdio: 'inherit' });
            } catch {
                console.log('  ⚠️  Playwright deps install failed (may need sudo)');
            }
        }

        console.log('  ✅ Agent Browser CLI installed!');
        return true;
    } catch {
        console.log('  ⚠️  Failed to install Agent Browser');
        console.log('  You can install manually: npm install -g @anthropic-ai/agent-browser');
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

    // Step 2: Wait for Docker to be running
    if (checkDocker()) {
        const dockerRunning = await waitForDocker(90); // Wait up to 90 seconds

        if (dockerRunning) {
            // Step 3: Setup Docker containers (in order)
            await setupDockerContainers();
        }
    }

    // Step 4: Check Docker services status
    checkDockerServices();

    // Step 5: Generate .env file
    generateEnvFile();

    // Step 6: Install Python package
    const pythonOk = installPythonPackage();

    // Step 7: Install Agent Browser CLI (replaces Playwright for AI agents)
    installAgentBrowser();

    // Step 8: Pull default model
    if (pythonOk && checkOllama()) {
        if (!checkModelInstalled(DEFAULT_MODEL)) {
            console.log(`\n  📥 Model ${DEFAULT_MODEL} not found.`);
            pullModel(DEFAULT_MODEL);
        } else {
            console.log(`  ✅ Model ${DEFAULT_MODEL}: Installed`);
        }
    }

    // Step 9: Launch CLI
    if (pythonOk) {
        launchCLI();
    } else {
        console.log('\n  Manual steps:');
        console.log('  pip install -e .');
        console.log('  itak\n');
    }
}

main();
