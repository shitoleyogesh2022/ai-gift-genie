# 🚀 Deploy AI Gift Genie to Render

## Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd ai_christmas_gift_generator
   git init
   git add .
   git commit -m "Initial commit - AI Gift Genie"
   ```

2. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-gift-genie.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy Backend on Render

1. **Go to [Render.com](https://render.com)** and sign up/login

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service**:
   - **Name**: `ai-gift-genie-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` (or paid for better performance)

5. **Add Environment Variable**:
   - Click "Environment" tab
   - Add: `GOOGLE_API_KEY` = `your_api_key_here`
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

6. **Click "Create Web Service"**

7. **Wait for deployment** (5-10 minutes)

8. **Copy your backend URL**: `https://ai-gift-genie-backend.onrender.com`

## Step 3: Update Frontend to Use Deployed Backend

1. **Edit `frontend/genz.html`**:
   - Find: `const API_URL = 'http://localhost:8003';`
   - Replace with: `const API_URL = 'https://ai-gift-genie-backend.onrender.com';`

2. **Commit and push**:
   ```bash
   git add frontend/genz.html
   git commit -m "Update API URL for production"
   git push
   ```

## Step 4: Deploy Frontend on Render

1. **Click "New +" → "Static Site"**

2. **Connect same GitHub repository**

3. **Configure**:
   - **Name**: `ai-gift-genie`
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: `echo "No build needed"`
   - **Publish Directory**: `frontend`

4. **Click "Create Static Site"**

5. **Your app is live!** 🎉
   - URL: `https://ai-gift-genie.onrender.com`

## Step 5: Test Your Deployment

1. Visit your frontend URL
2. Try generating gifts and messages
3. Test social sharing features

## 🎯 Quick Deploy (Alternative - Single Service)

Deploy both frontend and backend together:

1. **Click "New +" → "Web Service"**
2. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Add Static Files**:
   - Render will serve `frontend/genz.html` at root

## 💡 Tips

- **Free tier**: Backend sleeps after 15 min of inactivity (first request takes ~30s)
- **Upgrade**: $7/month for always-on service
- **Custom domain**: Add in Render dashboard settings
- **HTTPS**: Automatically enabled by Render

## 🔧 Troubleshooting

**Backend not responding?**
- Check logs in Render dashboard
- Verify GOOGLE_API_KEY is set
- Ensure requirements.txt is in root

**CORS errors?**
- Backend already has CORS enabled for all origins
- Check API_URL in frontend matches backend URL

**API key issues?**
- Verify key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check environment variables in Render dashboard

## 🎄 You're Done!

Share your app:
- `https://ai-gift-genie.onrender.com`

Enjoy spreading Christmas joy! 🎁✨