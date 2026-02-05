#!/usr/bin/env bash
# Post-installation configuration for OpenClaw on Linux systems
# Creates system-wide terminal launcher in standard binary path

APPLICATION_ROOT="/opt/OpenClaw"
LAUNCHER_TARGET="/usr/local/bin/openclaw"

# Verify installation directory accessibility
if [ ! -d "$APPLICATION_ROOT" ]; then
    echo "Warning: Expected application directory not found: $APPLICATION_ROOT" >&2
    exit 1
fi

# Generate terminal launcher with error handling
{
    echo '#!/usr/bin/env bash'
    echo '# Generated terminal launcher for OpenClaw desktop application'
    echo ''
    echo 'APP_LOCATION="/opt/OpenClaw"'
    echo 'APP_BINARY="$APP_LOCATION/openclaw"'
    echo ''
    echo 'if [ ! -x "$APP_BINARY" ]; then'
    echo '    echo "ERROR: Application binary not executable or missing" >&2'
    echo '    echo "Expected location: $APP_BINARY" >&2'
    echo '    exit 127'
    echo 'fi'
    echo ''
    echo 'exec "$APP_BINARY" --headless "$@"'
} > "$LAUNCHER_TARGET"

# Set execution permissions on launcher
chmod 755 "$LAUNCHER_TARGET"

# Verify launcher was created successfully
if [ -x "$LAUNCHER_TARGET" ]; then
    echo "Terminal launcher deployed successfully: $LAUNCHER_TARGET"
    echo "Command 'openclaw' is now available in your shell"
else
    echo "Warning: Launcher creation may have failed" >&2
    exit 1
fi

exit 0
