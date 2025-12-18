from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Optional
import warnings
from datetime import datetime

# Suppress deprecation warning
warnings.filterwarnings('ignore', category=FutureWarning)

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-flash')

app = FastAPI(title="🎄 AI Christmas Gift Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GiftRequest(BaseModel):
    recipient_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    relationship: str
    interests: List[str] = []
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    occasion: str = "Christmas"
    personality: Optional[str] = None
    special_notes: Optional[str] = None
    location: Optional[str] = None
    currency: str = "USD"

class MessageRequest(BaseModel):
    recipient_name: str
    relationship: str
    occasion: str = "Christmas"
    tone: str = "warm"
    gift_context: Optional[str] = None
    special_message: Optional[str] = None
    is_premium: bool = False

# Track free message usage (in production, use database)
free_messages_used = 0
MAX_FREE_MESSAGES = 3

# Sample messages for free users (dynamic year)
def get_sample_messages():
    next_year = datetime.now().year + 1
    return [
        f"Wishing you a Christmas filled with joy, laughter, and all the warmth of the season! May your holidays sparkle with happiness and your {next_year} be bright with new possibilities. 🎄✨",
        f"May this Christmas bring you peace, love, and countless moments of joy with those who matter most. Here's to a wonderful holiday season and an amazing {next_year} ahead! 🎅🎁",
        f"Sending warm Christmas wishes your way! May your heart be light, your days be merry, and your celebrations be filled with love and laughter. Happy holidays and a fantastic {next_year}! ❄️💕"
    ]

@app.get("/api")
async def root():
    return {"message": "🎄 AI Christmas Gift Generator API", "status": "running"}

@app.get("/")
async def serve_frontend():
    frontend_path = Path(__file__).parent.parent / "frontend" / "genz.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"error": "Frontend not found"}

@app.post("/reset-free-messages")
async def reset_free_messages():
    """Reset free message counter (for demo purposes)"""
    global free_messages_used
    free_messages_used = 0
    return {"message": "Free messages reset", "free_messages_used": free_messages_used}

@app.get("/list-models")
async def list_models():
    try:
        models = genai.list_models()
        model_list = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        return {"models": model_list}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test")
async def test():
    try:
        response = model.generate_content("Say hello in one word")
        return {"status": "success", "response": response.text, "model": model.model_name}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/generate-gifts")
async def generate_gifts(request: GiftRequest):
    print(f"\n=== GIFT REQUEST RECEIVED ===")
    print(f"Recipient: {request.recipient_name}")
    print(f"Interests: {request.interests}")
    try:
        print(f"Generating gifts for {request.recipient_name}...")
        
        currency_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'INR': '₹', 'JPY': '¥', 'AUD': 'A$', 'CAD': 'C$', 'CNY': '¥', 'AED': 'د.إ'}
        currency_symbol = currency_symbols.get(request.currency, '$')
        
        prompt = f"""Generate 3 gift ideas for {request.recipient_name} for {request.occasion}.

Details:
- Age: {request.age or 'Not specified'}
- Relationship: {request.relationship}
- Interests: {', '.join(request.interests) if request.interests else 'General'}
- Location: {request.location or 'Not specified'}
- Budget: {currency_symbol}{request.budget_min or 20} - {currency_symbol}{request.budget_max or 100} ({request.currency})
- Personality: {request.personality or 'Friendly'}

For each gift, provide:
1. Name
2. Description (1-2 sentences)
3. Why it's perfect
4. Price estimate (MUST use {request.currency} currency with {currency_symbol} symbol)
5. Where to buy (consider location: {request.location or 'general'})

IMPORTANT: All prices MUST be in {request.currency} currency using {currency_symbol} symbol.
Format each gift clearly numbered 1-3."""
        
        print("Calling Gemini API...")
        response = model.generate_content(prompt)
        text = response.text
        print(f"Response: {text[:200]}...")
        
        # Simple parser
        gifts = []
        lines = text.split('\n')
        current = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # New gift starts
            if line[0].isdigit() and '.' in line[:3]:
                if current and 'name' in current:
                    gifts.append(current)
                current = {'name': line.split('.', 1)[1].strip() if '.' in line else line}
            elif current:
                # Add to description
                if 'description' not in current:
                    current['description'] = line
                elif 'reason' not in current:
                    current['reason'] = line
                elif 'price_range' not in current:
                    current['price_range'] = line
                elif 'where_to_buy' not in current:
                    current['where_to_buy'] = line
        
        if current and 'name' in current:
            gifts.append(current)
        
        # Ensure all gifts have required fields
        for gift in gifts:
            gift.setdefault('description', 'A thoughtful gift')
            gift.setdefault('reason', 'Perfect for them')
            gift.setdefault('price_range', f"{currency_symbol}{request.budget_min or 20}-{currency_symbol}{request.budget_max or 100}")
            gift.setdefault('where_to_buy', 'Online or local stores')
        
        print(f"Parsed {len(gifts)} gifts")
        return {"gifts": gifts[:3], "recipient": request.recipient_name}
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-message")
async def generate_message(request: MessageRequest):
    global free_messages_used
    print(f"\n=== MESSAGE REQUEST RECEIVED ===")
    print(f"Recipient: {request.recipient_name}")
    
    try:
        # Check if user has premium or if they've exceeded free limit
        if not request.is_premium and free_messages_used >= MAX_FREE_MESSAGES:
            return {
                "message": None,
                "recipient": request.recipient_name,
                "requires_subscription": True,
                "sample_messages": get_sample_messages(),
                "free_messages_used": free_messages_used,
                "max_free_messages": MAX_FREE_MESSAGES
            }
        
        # For free users, return personalized sample message
        if not request.is_premium:
            free_messages_used += 1
            next_year = datetime.now().year + 1
            
            # Create personalized sample based on user inputs
            if request.tone == "funny":
                sample_message = f"Ho ho ho {request.recipient_name}! 🎅 Hope your Christmas is merrier than Santa after milk and cookies, and may {next_year} bring you more joy than a kid in a candy store! 🍭🎄"
            elif request.tone == "formal":
                sample_message = f"Dear {request.recipient_name}, I extend my warmest wishes for a joyous Christmas celebration and a prosperous {next_year}. May this festive season bring you peace and happiness. 🎄✨"
            elif request.tone == "heartfelt":
                sample_message = f"My dear {request.recipient_name}, Christmas reminds me how grateful I am to have you in my life. Wishing you all the love and warmth this season brings, and a beautiful {next_year} ahead. 💕🎄"
            else:  # warm
                sample_message = f"Merry Christmas, {request.recipient_name}! 🎄 May your holidays be filled with love, laughter, and all your favorite things. Here's to an amazing {next_year} together! ✨"
            
            return {
                "message": sample_message,
                "recipient": request.recipient_name,
                "is_sample": True,
                "free_messages_used": free_messages_used,
                "max_free_messages": MAX_FREE_MESSAGES
            }
        
        # Premium users get AI-generated messages
        print(f"Generating AI message for {request.recipient_name}...")
        current_year = datetime.now().year
        next_year = current_year + 1
        current_month = datetime.now().month
        
        # Smart context based on timing
        if current_month == 12:  # December
            time_context = f"It's December {current_year}, Christmas is here/approaching, and {next_year} is just around the corner."
        elif current_month == 1:  # January
            time_context = f"It's January {current_year}, the new year has just begun, and we're reflecting on the holidays."
        else:
            time_context = f"It's {current_year}, and we're looking forward to the upcoming holiday season and {next_year}."
        
        prompt = f"""Write a {request.tone} {request.occasion} message for {request.recipient_name}.
        
Relationship: {request.relationship}
Gift context: {request.gift_context or 'None'}
Special note: {request.special_message or 'None'}
Timing context: {time_context}

Use appropriate tense and timing references. Write a warm, personal message (2-4 sentences). Just the message, no quotes."""
        
        print("Calling Gemini API...")
        response = model.generate_content(prompt)
        message = response.text.strip().strip('"').strip("'")
        print(f"Message: {message[:100]}...")
        
        return {"message": message, "recipient": request.recipient_name, "is_premium": True}
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)