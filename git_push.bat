@echo off
git add .
set /p message="Commit message: "
git commit -m "%message%"
git push
