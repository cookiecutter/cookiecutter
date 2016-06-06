@echo off
set hooks_dir=%~dp0
set hooks_dir=%hooks_dir:~0,-1%
for %%F in ("%hooks_dir%") do set template_dir=%%~dpF
set template_dir=%template_dir:~0,-1%
echo %template_dir% >%cd%\batch
