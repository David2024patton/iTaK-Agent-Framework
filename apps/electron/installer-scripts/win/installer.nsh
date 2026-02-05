; NSIS installer customization for iTaK Agent
; This script adds the CLI to Windows PATH

!macro customInstall
  ; Add iTaK CLI directory to system PATH
  ; The installer will place itak.cmd in this directory
  
  DetailPrint "Installing iTaK CLI to PATH..."
  
  ; Copy the CLI batch script to install directory
  SetOutPath "$INSTDIR"
  File "${BUILD_RESOURCES_DIR}\installer-scripts\win\itak.cmd"
  
  ; Add to PATH
  ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR"
  
  DetailPrint "iTaK CLI installed. You can now use 'itak' command from any terminal."
!macroend

!macro customUnInstall
  ; Remove from PATH
  ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR"
!macroend
