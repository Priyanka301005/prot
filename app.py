from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ==============================
# Gmail Configuration
# ==============================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'makawanapriyanka3010@gmail.com'
app.config['MAIL_PASSWORD'] = 'gafj jcag rjei eyly'
app.config['MAIL_DEFAULT_SENDER'] = 'makawanapriyanka3010@gmail.com'

mail = Mail(app)

# ==============================
# Home Page
# ==============================

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# ==============================
# Contact Form API
# ==============================

@app.route('/api/contact', methods=['POST'])
def contact():

    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Please fill all fields."
            }), 400

        # Email to you
        admin_email = Message(
            subject=f"New Portfolio Contact - {name}",
            recipients=["makawanapriyanka3010@gmail.com"]
        )

        admin_email.body = f"""
New Contact Form Submission

Name:
{name}

Email:
{email}

Message:
{message}
"""

        mail.send(admin_email)

        # Confirmation Email
        user_email = Message(
            subject="Thank you for contacting me",
            recipients=[email]
        )

        user_email.body = f"""
Hello {name},

Thank you for contacting me.

I have received your message.

I will reply as soon as possible.

Regards,

Priyanka Makawana
Data Scientist
"""

        mail.send(user_email)

        return jsonify({
            "success": True,
            "message": "Message sent successfully."
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==============================
# Run Server
# ==============================

if __name__ == "__main__":

    print("=" * 60)
    print("Portfolio Server Started")
    print("Website : http://127.0.0.1:5000")
    print("=" * 60)

    app.run(debug=True)