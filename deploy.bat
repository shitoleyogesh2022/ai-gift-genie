@echo off
echo ========================================
echo   AI Gift Genie - GitHub Deployment
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Initializing Git...
git init

echo.
echo Step 2: Adding files...
git add .

echo.
echo Step 3: Creating commit...
git commit -m "Initial commit - AI Gift Genie Christmas App"

echo.
echo Step 4: Setting up remote...
git remote add origin https://github.com/shitoleyogesh2022/ai-gift-genie.git

echo.
echo Step 5: Renaming branch to main...
git branch -M main

echo.
echo Step 6: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Go to https://render.com
echo 2. Click "New +" - "Web Service"
echo 3. Connect your GitHub repo
echo 4. Use these settings:
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: cd backend ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo    - Add Environment Variable: GOOGLE_API_KEY
echo.
pause