; Windows installer customization for OpenClaw desktop application
; Provides terminal access by creating command wrapper and updating environment

!macro customInstall
  ; Build batch wrapper for terminal invocation
  Var /GLOBAL shimFileHandle
  StrCpy $shimFileHandle "$INSTDIR\openclaw.cmd"
  FileOpen $0 $shimFileHandle w
  FileWrite $0 "@echo off$\r$\n"
  FileWrite $0 "REM Terminal wrapper - invokes desktop app in headless CLI mode$\r$\n"
  FileWrite $0 'if "%1"=="" ($\r$\n'
  FileWrite $0 '  echo Usage: openclaw [command] [options]$\r$\n'
  FileWrite $0 '  exit /b 1$\r$\n'
  FileWrite $0 ')$\r$\n'
  FileWrite $0 'start /wait /b "$INSTDIR\OpenClaw.exe" --headless %*$\r$\n'
  FileClose $0

  ; Register directory in machine-level environment path variable
  EnVar::SetHKLM
  EnVar::AddValue "PATH" "$INSTDIR"
  Pop $0
  
  DetailPrint "Command wrapper created at: $shimFileHandle"
  DetailPrint "Installation directory registered in system PATH"
  DetailPrint "Terminal sessions must be restarted to recognize 'openclaw' command"
!macroend

!macro customUnInstall
  Var /GLOBAL cleanupShimPath
  StrCpy $cleanupShimPath "$INSTDIR\openclaw.cmd"
  Delete $cleanupShimPath
  
  EnVar::SetHKLM
  EnVar::DeleteValue "PATH" "$INSTDIR"
  Pop $0
  
  DetailPrint "Command wrapper removed from installation"
  DetailPrint "Installation path removed from system environment"
!macroend
