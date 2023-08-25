@echo off

REM change directory to repo
cd /d "C:\Code\ajhalling\mwii-time-tracker"

REM run refresh_data script to update .csv
python dash\scripts\refresh_data.py

REM Add all changes (including the updated local file)
git add -A

REM Commit the changes with a message
git commit -m "Update: %date% from HTPC"

REM Push the changes to the remote repository using the PAT from environment variable
git push origin master -c http.extraheader="Authorization: Bearer %GITHUB_PAT%"
