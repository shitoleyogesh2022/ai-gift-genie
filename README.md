# 🎄 AI Gift Genie - Christmas Gift & Message Generator

An AI-powered web app that generates personalized Christmas gift suggestions and heartfelt messages using Google Gemini AI.

## ✨ Features

- 🎁 **Smart Gift Suggestions** - AI-powered personalized gift recommendations
- 💌 **Message Generator** - Create heartfelt Christmas/New Year messages
- 🌍 **Multi-Currency Support** - USD, EUR, GBP, INR, JPY, AUD, CAD, CNY, AED
- 📍 **Location-Based** - Prices and availability based on location
- 🎨 **GenZ UI** - Modern, animated interface with 3D effects
- 🤖 **AI Robot Animation** - Cute thinking animation while generating
- 📱 **Social Sharing** - Share on WhatsApp, Facebook, Twitter, Telegram, Instagram
- 🎯 **Interest-Based** - Select from 12 interest categories
- 💰 **Budget-Aware** - Respects your spending limits

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai_christmas_gift_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create `.env` file:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the backend**
   ```bash
   python backend/main.py
   ```

5. **Open the frontend**
   - Open `frontend/genz.html` in your browser
   - Or visit `http://localhost:8003` if serving static files

## 🌐 Deploy to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Create Web Service on Render
3. Add `GOOGLE_API_KEY` environment variable
4. Deploy! 🎉

## 🎯 How to Use

### Gift Finder
1. Enter recipient details (name, age, relationship)
2. Select their interests from 12 categories
3. Choose location and currency
4. Set budget range
5. Click "Find Perfect Gifts"
6. Get 5 personalized gift suggestions with prices

### Message Maker
1. Enter recipient name and relationship
2. Choose occasion (Christmas/New Year/Both)
3. Select tone (Warm/Funny/Formal/Heartfelt)
4. Add optional gift context
5. Click "Create Message"
6. Get a personalized heartfelt message

### Share Results
- Click any social media button to share
- Copy to clipboard for Instagram
- Share on WhatsApp, Facebook, Twitter, Telegram

## 🛠️ Tech Stack

- **Frontend**: React (CDN), Vanilla CSS, HTML5
- **Backend**: FastAPI, Python 3.12
- **AI**: Google Gemini 2.5 Flash
- **Deployment**: Render.com
- **Icons**: Font Awesome

## 📁 Project Structure

```
ai_christmas_gift_generator/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── genz.html           # React frontend (single file)
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Root requirements
├── Procfile              # Heroku config
├── render.yaml           # Render config
├── DEPLOYMENT.md         # Deployment guide
└── README.md            # This file
```

## 🎨 Features Showcase

### UI/UX
- Animated floating Christmas shapes (🎁🎄⭐🎅❄️)
- 3D robot with moving eyes and waving arms
- Smooth transitions and hover effects
- Gradient backgrounds and glass morphism
- Responsive design for all devices

### AI Capabilities
- Context-aware gift suggestions
- Budget and location-based recommendations
- Personality-matched gifts
- Tone-appropriate messages
- Multi-language currency support

## 🔑 API Endpoints

- `GET /` - Health check
- `GET /test` - Test Gemini connection
- `GET /list-models` - List available AI models
- `POST /generate-gifts` - Generate gift suggestions
- `POST /generate-message` - Generate personalized message

## 💡 Tips

- Be specific with interests for better suggestions
- Add personality traits for more accurate matching
- Use location for region-specific recommendations
- Try different tones for varied message styles

## 🐛 Troubleshooting

**Backend not starting?**
- Check if port 8003 is available
- Verify GOOGLE_API_KEY is set
- Install all requirements

**No results generated?**
- Check backend logs for errors
- Verify API key is valid
- Check internet connection

**CORS errors?**
- Ensure backend is running
- Check API_URL in frontend matches backend

## 📝 License

MIT License - Feel free to use and modify!

## 🎄 Credits

Built with ❤️ using Google Gemini AI

Enjoy spreading Christmas joy! 🎁✨