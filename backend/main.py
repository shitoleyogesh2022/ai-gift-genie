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
import random
import uuid

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

class SecretSantaRequest(BaseModel):
    names: List[str]
    exclude_pairs: Optional[List[List[str]]] = None  # [["John", "Jane"]] means John can't be Jane's Santa

class PartyPlannerRequest(BaseModel):
    occasion: str  # Christmas, New Year, Birthday, etc.
    guest_count: int
    budget: Optional[float] = None
    venue_type: str  # home, restaurant, outdoor, etc.
    theme: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    age_group: str  # kids, adults, mixed, seniors

class BudgetItem(BaseModel):
    name: str
    category: str  # gifts, food, decorations, etc.
    planned_amount: float
    actual_amount: Optional[float] = None
    recipient: Optional[str] = None

class BudgetRequest(BaseModel):
    total_budget: float
    currency: str = "USD"
    items: List[BudgetItem] = []

class WishlistRequest(BaseModel):
    title: str
    items: List[str]
    occasion: str
    privacy: str = "public"  # public, private, friends

class CaptionRequest(BaseModel):
    photo_description: str
    occasion: str
    tone: str = "fun"  # fun, heartfelt, funny, elegant
    hashtags: bool = True

class WishlistRequest(BaseModel):
    title: str
    items: List[str]
    occasion: str = "Christmas"
    recipient_name: str
    privacy: str = "public"  # public, private, friends

class CardRequest(BaseModel):
    occasion: str  # Christmas, New Year, Birthday, etc.
    recipient_name: str
    sender_name: str
    relationship: str
    tone: str = "warm"  # warm, funny, formal, heartfelt
    custom_message: Optional[str] = None
    card_style: str = "classic"  # classic, modern, cute, elegant

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

@app.post("/party-planner")
async def generate_party_plan(request: PartyPlannerRequest):
    print(f"\n=== PARTY PLANNER REQUEST ===")
    try:
        prompt = f"""Create a comprehensive {request.occasion} party plan for {request.guest_count} guests.
        
Details:
        - Budget: ${request.budget or 'Flexible'}
        - Venue: {request.venue_type}
        - Theme: {request.theme or 'Classic'}
        - Age group: {request.age_group}
        - Dietary restrictions: {request.dietary_restrictions or 'None'}
        
Provide:
        1. Theme & Decorations (3-4 ideas)
        2. Food & Drinks Menu (5-6 items)
        3. Activities & Games (4-5 options)
        4. Timeline (hour by hour)
        5. Shopping List (essentials)
        
Make it creative, engaging, and budget-conscious. Format clearly with emojis."""
        
        response = model.generate_content(prompt)
        plan = response.text.strip()
        
        return {"party_plan": plan, "occasion": request.occasion, "guests": request.guest_count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/budget-tracker")
async def track_budget(request: BudgetRequest):
    try:
        total_planned = sum(item.planned_amount for item in request.items)
        total_actual = sum(item.actual_amount or 0 for item in request.items)
        remaining = request.total_budget - total_actual
        
        categories = {}
        for item in request.items:
            if item.category not in categories:
                categories[item.category] = {"planned": 0, "actual": 0, "items": []}
            categories[item.category]["planned"] += item.planned_amount
            categories[item.category]["actual"] += item.actual_amount or 0
            categories[item.category]["items"].append(item.dict())
        
        return {
            "total_budget": request.total_budget,
            "total_planned": total_planned,
            "total_spent": total_actual,
            "remaining": remaining,
            "categories": categories,
            "currency": request.currency,
            "over_budget": total_actual > request.total_budget
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/photo-caption")
async def generate_caption(request: CaptionRequest):
    try:
        hashtag_prompt = "Include 5-8 relevant hashtags" if request.hashtags else "No hashtags"
        
        prompt = f"""Create a {request.tone} social media caption for a {request.occasion} photo.
        
Photo description: {request.photo_description}
Tone: {request.tone}
{hashtag_prompt}

Make it engaging, shareable, and authentic. 1-2 sentences max."""
        
        response = model.generate_content(prompt)
        caption = response.text.strip().strip('"').strip("'")
        
        return {"caption": caption, "occasion": request.occasion}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-wishlist")
async def create_wishlist(request: WishlistRequest):
    try:
        wishlist_id = str(uuid.uuid4())[:8]
        
        # Generate smart suggestions based on items
        prompt = f"""Analyze this {request.occasion} wishlist for {request.recipient_name} and provide:
        1. 3 additional gift suggestions that complement the existing items
        2. Budget estimate for the wishlist
        3. Priority ranking of items (most wanted to least)
        
        Wishlist items: {', '.join(request.items)}
        
        Format clearly with emojis and be helpful."""
        
        response = model.generate_content(prompt)
        suggestions = response.text.strip()
        
        return {
            "wishlist_id": wishlist_id,
            "title": request.title,
            "items": request.items,
            "recipient": request.recipient_name,
            "occasion": request.occasion,
            "ai_suggestions": suggestions,
            "share_url": f"ai-gift-genie.onrender.com/wishlist/{wishlist_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-card")
async def generate_card(request: CardRequest):
    print(f"\n=== CARD REQUEST RECEIVED ===")
    print(f"From: {request.sender_name} To: {request.recipient_name}")
    print(f"Occasion: {request.occasion}, Style: {request.card_style}")
    try:
        prompt = f"""Create a beautiful {request.occasion} card message from {request.sender_name} to {request.recipient_name}.
        
Relationship: {request.relationship}
Tone: {request.tone}
Card style: {request.card_style}
Custom message: {request.custom_message or 'None'}

Generate:
1. Front cover text (short, catchy)
2. Inside message (heartfelt, 2-3 sentences)
3. Closing signature suggestion

Make it {request.tone} and appropriate for their {request.relationship} relationship."""
        
        print("Calling Gemini API for card...")
        response = model.generate_content(prompt)
        card_content = response.text.strip()
        print(f"Card generated: {card_content[:100]}...")
        
        return {
            "card_content": card_content,
            "occasion": request.occasion,
            "style": request.card_style,
            "recipient": request.recipient_name,
            "sender": request.sender_name
        }
        
    except Exception as e:
        print(f"CARD ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/secret-santa")
async def generate_secret_santa(request: SecretSantaRequest):
    print(f"\n=== SECRET SANTA REQUEST ===")
    print(f"Participants: {len(request.names)}")
    try:
        import random
        
        if len(request.names) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 participants")
        
        givers = request.names.copy()
        receivers = request.names.copy()
        assignments = {}
        max_attempts = 100
        
        for attempt in range(max_attempts):
            random.shuffle(receivers)
            valid = True
            temp_assignments = {}
            
            for i, giver in enumerate(givers):
                receiver = receivers[i]
                
                # Can't give to yourself
                if giver == receiver:
                    valid = False
                    break
                
                # Check exclusions
                if request.exclude_pairs:
                    for pair in request.exclude_pairs:
                        if giver in pair and receiver in pair:
                            valid = False
                            break
                
                if not valid:
                    break
                    
                temp_assignments[giver] = receiver
            
            if valid:
                assignments = temp_assignments
                break
        
        if not assignments:
            raise HTTPException(status_code=400, detail="Could not generate valid assignments. Try removing some exclusions.")
        
        # Format results
        results = [{"giver": k, "receiver": v} for k, v in assignments.items()]
        
        return {
            "success": True,
            "assignments": results,
            "total_participants": len(request.names)
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
        
        # For free users, generate personalized message using AI but mark as sample
        if not request.is_premium:
            free_messages_used += 1
            
            # Generate actual personalized message for free users too
            current_year = datetime.now().year
            next_year = current_year + 1
            current_month = datetime.now().month
            
            if current_month == 12:
                time_context = f"Current year: {current_year} (December), upcoming new year: {next_year}. Christmas is here/approaching."
            elif current_month == 1:
                time_context = f"Current year: {current_year} (January), we just entered this new year from {current_year-1}."
            else:
                time_context = f"Current year: {current_year}, upcoming new year will be: {next_year}."
            
            prompt = f"""Write a {request.tone} {request.occasion} message for {request.recipient_name}.
            
Relationship: {request.relationship}
Gift context: {request.gift_context or 'None'}
Special note: {request.special_message or 'None'}
Timing context: {time_context}

IMPORTANT: Use correct year references - we are currently in {current_year}, and the upcoming new year is {next_year}. Write a warm, personal message (2-4 sentences). Just the message, no quotes."""
            
            response = model.generate_content(prompt)
            sample_message = response.text.strip().strip('"').strip("'")
            
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
        if current_month == 12:
            time_context = f"Current year: {current_year} (December), upcoming new year: {next_year}. Christmas is here/approaching."
        elif current_month == 1:
            time_context = f"Current year: {current_year} (January), we just entered this new year from {current_year-1}."
        else:
            time_context = f"Current year: {current_year}, upcoming new year will be: {next_year}."
        
        prompt = f"""Write a {request.tone} {request.occasion} message for {request.recipient_name}.
        
Relationship: {request.relationship}
Gift context: {request.gift_context or 'None'}
Special note: {request.special_message or 'None'}
Timing context: {time_context}

IMPORTANT: Use correct year references - we are currently in {current_year}, and the upcoming new year is {next_year}. Write a warm, personal message (2-4 sentences). Just the message, no quotes."""
        
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