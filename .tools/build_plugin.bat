@echo off
setlocal EnableExtensions

set "src=%~1"
if not defined src (
  echo Usage: build_plugin.bat ^<plugin.py^|PluginFolder^>
  exit /b 1
)

if /i "%~x1"==".py" goto :build

if exist "%~1\" (
  for %%f in ("%~1\*.py") do (
    set "src=%%~ff"
    goto :build
  )
  echo No .py found in: %~1
  exit /b 1
)

echo Not found: %~1
exit /b 1

:build
for %%I in ("%src%") do (
  copy /Y "%src%" "%%~dpnI.plugin" >nul
  if errorlevel 1 (
    echo Build failed: %src%
    exit /b 1
  )
  echo Built: %%~dpnI.plugin
)
exit /b 0
