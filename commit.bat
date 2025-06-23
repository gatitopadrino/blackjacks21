@echo off
echo Adding changes...
git add .

echo Committing changes...
git commit -m "Update blackjack.py with image scaling and bug fixes"

echo Pulling latest changes from remote...
git pull origin main --rebase

echo Pushing changes to remote...
git push origin main

echo Done!
pause
