@echo off
rem ===================================================================
rem  Plan Expert — script OEM execute a la fin de l'installation Windows
rem  Journal : C:\OEM\install.log
rem ===================================================================
set "LOG=C:\OEM\install.log"
echo ================================================= >> "%LOG%" 2>&1
echo [%DATE% %TIME%] install.bat debut >> "%LOG%" 2>&1

rem --- 1) Copie de Plan Expert vers Program Files (x86) ---------------
if exist "C:\OEM\PlanExpert\PlanExpert.exe" (
  echo [%TIME%] copie Plan Expert >> "%LOG%" 2>&1
  if not exist "C:\Program Files (x86)\Plan Expert" mkdir "C:\Program Files (x86)\Plan Expert"
  xcopy "C:\OEM\PlanExpert\*" "C:\Program Files (x86)\Plan Expert\" /E /I /Y /Q >> "%LOG%" 2>&1
) else (
  echo [%TIME%] ATTENTION : C:\OEM\PlanExpert\PlanExpert.exe introuvable >> "%LOG%" 2>&1
)

rem --- 2) Reste de la configuration en PowerShell ---------------------
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\OEM\post-install.ps1" >> "%LOG%" 2>&1
echo [%DATE% %TIME%] install.bat fin (code %ERRORLEVEL%) >> "%LOG%" 2>&1
exit /b 0
