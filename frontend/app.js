const { useState } = React;
const API_URL = 'http://localhost:8003';

const giftEmojis = {
    'Technology': '💻', 'Reading': '📚', 'Sports': '⚽', 'Music': '🎵',
    'Art': '🎨', 'Cooking': '👨‍🍳', 'Travel': '✈️', 'Gaming': '🎮',
    'Fashion': '👗', 'Fitness': '💪', 'Photography': '📸', 'Gardening': '🌱'
};

function RobotThinking() {
    return (
        <div className="robot-container">
            <div className="robot">
                <div className="robot-head">
                    <div className="robot-antenna"></div>
                    <div className="robot-eyes">
                        <div className="robot-eye"></div>
                        <div className="robot-eye"></div>
                    </div>
                    <div className="robot-mouth"></div>
                </div>
                <div className="robot-body">
                    <div className="robot-arm left"></div>
                    <div className="robot-arm right"></div>
                </div>
            </div>
            <div className="thinking-text">AI is thinking...</div>
            <div className="thinking-dots">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
            </div>
        </div>
    );
}

function App() {
    const [activeTab, setActiveTab] = useState('gifts');
    const [loading, setLoading] = useState(false);
    const [gifts, setGifts] = useState([]);
    const [message, setMessage] = useState('');
    
    const [giftForm, setGiftForm] = useState({
        recipient_name: '',
        age: '',
        gender: '',
        relationship: 'friend',
        interests: [],
        budget_min: '',
        budget_max: '',
        occasion: 'Christmas',
        personality: '',
        special_notes: ''
    });

    const [messageForm, setMessageForm] = useState({
        recipient_name: '',
        relationship: 'friend',
        occasion: 'Christmas',
        tone: 'warm',
        gift_context: '',
        special_message: ''
    });

    const interestOptions = Object.keys(giftEmojis);

    const toggleInterest = (interest) => {
        setGiftForm(prev => ({
            ...prev,
            interests: prev.interests.includes(interest)
                ? prev.interests.filter(i => i !== interest)
                : [...prev.interests, interest]
        }));
    };

    const handleGenerateGifts = async (e) => {
        e.preventDefault();
        setLoading(true);
        setGifts([]);

        try {
            const response = await fetch(`${API_URL}/generate-gifts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...giftForm,
                    age: giftForm.age ? parseInt(giftForm.age) : null,
                    budget_min: giftForm.budget_min ? parseFloat(giftForm.budget_min) : null,
                    budget_max: giftForm.budget_max ? parseFloat(giftForm.budget_max) : null
                })
            });

            const data = await response.json();
            setGifts(data.gifts);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateMessage = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            const response = await fetch(`${API_URL}/generate-message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(messageForm)
            });

            const data = await response.json();
            setMessage(data.message);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="floating-shapes">
                {[...Array(5)].map((_, i) => (
                    <div key={i} className="shape" style={{fontSize: '5em'}}>
                        {['🎁', '🎄', '⭐', '🎅', '❄️'][i]}
                    </div>
                ))}
            </div>

            <div className="container">
                <div className="header">
                    <h1>🎁 AI Gift Genie ✨</h1>
                    <p className="subtitle">Your AI-powered Christmas gift wizard</p>
                </div>

                <div className="main-grid">
                    <div className="card">
                        <div className="card-header">
                            <div className="card-icon">🎁</div>
                            <div className="card-title">Gift Finder</div>
                        </div>

                        <form onSubmit={handleGenerateGifts}>
                            <div className="form-row">
                                <div className="form-group">
                                    <label>🎯 Recipient Name</label>
                                    <input 
                                        type="text" 
                                        required
                                        value={giftForm.recipient_name}
                                        onChange={(e) => setGiftForm({...giftForm, recipient_name: e.target.value})}
                                        placeholder="e.g., Sarah"
                                    />
                                </div>
                                <div className="form-group">
                                    <label>🎂 Age</label>
                                    <input 
                                        type="number"
                                        value={giftForm.age}
                                        onChange={(e) => setGiftForm({...giftForm, age: e.target.value})}
                                        placeholder="25"
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>👤 Relationship</label>
                                    <select 
                                        value={giftForm.relationship}
                                        onChange={(e) => setGiftForm({...giftForm, relationship: e.target.value})}
                                    >
                                        <option value="friend">Friend</option>
                                        <option value="family">Family</option>
                                        <option value="colleague">Colleague</option>
                                        <option value="partner">Partner</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>🎄 Occasion</label>
                                    <select 
                                        value={giftForm.occasion}
                                        onChange={(e) => setGiftForm({...giftForm, occasion: e.target.value})}
                                    >
                                        <option value="Christmas">Christmas</option>
                                        <option value="New Year">New Year</option>
                                        <option value="Both">Both</option>
                                    </select>
                                </div>
                            </div>

                            <div className="form-group">
                                <label>💖 Interests</label>
                                <div className="interests-grid">
                                    {interestOptions.map(interest => (
                                        <button 
                                            key={interest}
                                            type="button"
                                            className={`interest-btn ${giftForm.interests.includes(interest) ? 'selected' : ''}`}
                                            onClick={() => toggleInterest(interest)}
                                        >
                                            {giftEmojis[interest]} {interest}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>💰 Min Budget</label>
                                    <input 
                                        type="number"
                                        value={giftForm.budget_min}
                                        onChange={(e) => setGiftForm({...giftForm, budget_min: e.target.value})}
                                        placeholder="$20"
                                    />
                                </div>
                                <div className="form-group">
                                    <label>💎 Max Budget</label>
                                    <input 
                                        type="number"
                                        value={giftForm.budget_max}
                                        onChange={(e) => setGiftForm({...giftForm, budget_max: e.target.value})}
                                        placeholder="$100"
                                    />
                                </div>
                            </div>

                            <button type="submit" className="generate-btn" disabled={loading}>
                                {loading ? '✨ Generating Magic...' : '🎁 Find Perfect Gifts'}
                            </button>
                        </form>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <div className="card-icon">💌</div>
                            <div className="card-title">Message Maker</div>
                        </div>

                        <form onSubmit={handleGenerateMessage}>
                            <div className="form-group">
                                <label>🎯 Recipient Name</label>
                                <input 
                                    type="text" 
                                    required
                                    value={messageForm.recipient_name}
                                    onChange={(e) => setMessageForm({...messageForm, recipient_name: e.target.value})}
                                    placeholder="e.g., John"
                                />
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>👤 Relationship</label>
                                    <select 
                                        value={messageForm.relationship}
                                        onChange={(e) => setMessageForm({...messageForm, relationship: e.target.value})}
                                    >
                                        <option value="friend">Friend</option>
                                        <option value="family">Family</option>
                                        <option value="colleague">Colleague</option>
                                        <option value="partner">Partner</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>🎭 Tone</label>
                                    <select 
                                        value={messageForm.tone}
                                        onChange={(e) => setMessageForm({...messageForm, tone: e.target.value})}
                                    >
                                        <option value="warm">Warm 🤗</option>
                                        <option value="funny">Funny 😂</option>
                                        <option value="formal">Formal 🎩</option>
                                        <option value="heartfelt">Heartfelt 💕</option>
                                    </select>
                                </div>
                            </div>

                            <div className="form-group">
                                <label>🎁 Gift Context (Optional)</label>
                                <input 
                                    type="text"
                                    value={messageForm.gift_context}
                                    onChange={(e) => setMessageForm({...messageForm, gift_context: e.target.value})}
                                    placeholder="e.g., I'm giving them a book"
                                />
                            </div>

                            <div className="form-group">
                                <label>✨ Special Message (Optional)</label>
                                <textarea 
                                    rows="3"
                                    value={messageForm.special_message}
                                    onChange={(e) => setMessageForm({...messageForm, special_message: e.target.value})}
                                    placeholder="Any memories or wishes..."
                                />
                            </div>

                            <button type="submit" className="generate-btn" disabled={loading}>
                                {loading ? '✨ Crafting Message...' : '💌 Create Message'}
                            </button>
                        </form>
                    </div>
                </div>

                {loading && <RobotThinking />}

                {!loading && gifts.length > 0 && (
                    <div className="gift-grid">
                        {gifts.map((gift, index) => (
                            <div key={index} className="gift-card">
                                <div className="gift-image">
                                    {['🎁', '🎀', '🎊', '🎉', '✨'][index]}
                                </div>
                                <div className="gift-content">
                                    <div className="gift-name">{gift.name}</div>
                                    <div className="gift-description">{gift.description}</div>
                                    <div className="gift-description"><strong>Why perfect:</strong> {gift.reason}</div>
                                    <div className="gift-price">💰 {gift.price_range}</div>
                                    <div className="gift-badge">🛒 {gift.where_to_buy}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {!loading && message && (
                    <div className="message-card">
                        <h2 style={{marginBottom: '20px', color: '#d63031'}}>💌 Your Heartfelt Message</h2>
                        <div className="message-text">{message}</div>
                    </div>
                )}
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));