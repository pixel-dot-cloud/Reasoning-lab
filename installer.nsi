!include "MUI2.nsh"

!define APP_NAME    "Reasoning Lab"
!define APP_VERSION "1.1.1"
!define APP_PUBLISHER "pixel-dot-cloud"
!define APP_EXE     "ReasoningLab.exe"
!define REG_KEY     "Software\${APP_PUBLISHER}\${APP_NAME}"
!define UNINST_KEY  "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

Name              "${APP_NAME} ${APP_VERSION}"
OutFile           "ReasoningLab-Setup.exe"
InstallDir        "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey  HKLM "${REG_KEY}" "InstallDir"
RequestExecutionLevel admin
Unicode true

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ---- Install ----------------------------------------------------------------
Section "Install" SecInstall
  SetOutPath "$INSTDIR"
  File /r "dist\ReasoningLab\*"

  ; Shortcuts
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
  CreateShortcut  "$DESKTOP\${APP_NAME}.lnk"                "$INSTDIR\${APP_EXE}"

  ; Uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Registry – install dir
  WriteRegStr HKLM "${REG_KEY}" "InstallDir" "$INSTDIR"

  ; Registry – Add/Remove Programs
  WriteRegStr   HKLM "${UNINST_KEY}" "DisplayName"     "${APP_NAME}"
  WriteRegStr   HKLM "${UNINST_KEY}" "DisplayVersion"  "${APP_VERSION}"
  WriteRegStr   HKLM "${UNINST_KEY}" "Publisher"       "${APP_PUBLISHER}"
  WriteRegStr   HKLM "${UNINST_KEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr   HKLM "${UNINST_KEY}" "DisplayIcon"     "$INSTDIR\${APP_EXE}"
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify"        1
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair"        1
SectionEnd

; ---- Uninstall --------------------------------------------------------------
Section "Uninstall"
  RMDir /r "$INSTDIR"

  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  RMDir  "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"

  DeleteRegKey HKLM "${UNINST_KEY}"
  DeleteRegKey HKLM "${REG_KEY}"
SectionEnd
