@echo off
set APPLICATION_UNDER_TEST=c:\temp\foobar.py
set AUTOPILOT_APP=c:\temp\autopilot\src\run.py
set MANUSCRIPTS=c:\temp\manuscripts

python %AUTOPILOT_APP%  -m foobar_manuscript.txt -p %MANUSCRIPTS%  %APPLICATION_UNDER_TEST%


