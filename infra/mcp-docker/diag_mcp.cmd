@echo off
rem Lance le diagnostic MCP dans l'environnement du Google Cloud SDK Shell (meme PATH que le raccourci).
call "C:\Users\fvegiard\AppData\Local\Google\Cloud SDK\cloud_env.bat"
set "PS=C:\Program Files\PowerShell\7\pwsh.exe"
if not exist "%PS%" set "PS=pwsh"
set "LOG=%USERPROFILE%\Desktop\_claude_mcp_diag.log"
"%PS%" -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Desktop\_claude_mcp_diag.ps1" > "%LOG%" 2>&1
echo EXIT=%ERRORLEVEL% >> "%LOG%"
