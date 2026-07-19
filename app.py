from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# File to store messages
MESSAGES_FILE = 'messages.txt'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Validate input
        if not name or not email or not message:
            return jsonify({'error': 'All fields are required'}), 400
        
        if '@' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Save message to text file
        with open(MESSAGES_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n{'='*60}\n")
            f.write(f"📅 DATE & TIME: {timestamp}\n")
            f.write(f"👤 NAME: {name}\n")
            f.write(f"📧 EMAIL: {email}\n")
            f.write(f"💬 MESSAGE:\n")
            f.write(f"{message}\n")
            f.write(f"{'='*60}\n")
        
        # Also print to console
        print(f"\n{'='*60}")
        print(f"✅ NEW MESSAGE RECEIVED!")
        print(f"📅 Time: {timestamp}")
        print(f"👤 From: {name}")
        print(f"📧 Email: {email}")
        print(f"💬 Message: {message[:100]}...")
        print(f"📁 Saved to: {MESSAGES_FILE}")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'message': f"Thank you {name}! Your message has been received. I'll respond within 24 hours."
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/view-messages')
def view_messages():
    """Simple page to view all messages"""
    if not os.path.exists(MESSAGES_FILE):
        return "<h1>No messages yet</h1><p>Send a test message first!</p><a href='/'>Back to Home</a>"
    
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Messages - Admin Panel</title>
        <style>
            body {{ font-family: 'Courier New', monospace; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            h1 {{ color: #1a5f7a; border-bottom: 2px solid #e67e22; padding-bottom: 10px; }}
            pre {{ background: #f9f9f9; padding: 15px; overflow-x: auto; border-left: 4px solid #e67e22; }}
            .back-btn {{ background: #1a5f7a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
            .back-btn:hover {{ background: #0f2b3d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📬 Contact Messages</h1>
            <pre>{content}</pre>
            <a href="/" class="back-btn">← Back to Portfolio</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DATA SCIENCE PORTFOLIO SERVER")
    print("="*60)
    print(f"📁 Current folder: {os.getcwd()}")
    print(f"📄 Messages will be saved to: {MESSAGES_FILE}")
    print("🌐 Main website: http://localhost:5000")
    print("👁️  View messages: http://localhost:5000/view-messages")
    print("="*60 + "\n")
    print("💡 Press CTRL+C to stop the server\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')