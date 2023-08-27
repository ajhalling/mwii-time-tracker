@echo off

REM Change directory to repo
echo Changing directory to repo...
cd /d "C:\Code\ajhalling\mwii-time-tracker"

REM Run refresh_data script to update .csv
echo Running refresh_data script...
cd dash\data
python ..\..\dash\scripts\refresh_data.py
cd ..

REM Add all changes (including the updated .csv file)
echo Adding changes to Git...
git add -A

REM Commit the changes with a message.
echo Committing changes...
git commit -m "Update: %date% from HTPC"

REM Set the GitHub Personal Access Token
set "GITHUB_PAT=YOUR_GITHUB_PAT_HERE"

REM Set the HTTP header with the GITHUB_PAT environment variable
set "GIT_HTTP_HEADER=Authorization: Bearer %GITHUB_PAT%"

REM Push the changes to the remote repository (using 'main' as the branch name)
echo Pushing changes to remote repository...
git push origin main

echo Script completed.
