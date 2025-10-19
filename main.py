import os
from flask import Flask, request, render_template
import logging
import requests
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import telebot
import threading
from flask import jsonify, url_for
from google_drive import GoogleDriveManager
from werkzeug.utils import secure_filename
import tempfile

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Get environment variables
token = os.environ.get("token")
CHAT_ID = os.environ.get("CHAT_ID")

# Initialize Telegram bot
bot = telebot.TeleBot(token)

# Initialize Google Drive
drive_manager = None
print("Initializing Google Drive manager...")
if os.path.exists('credentials.json'):
    try:
        print("Found credentials.json, attempting to initialize...")
        drive_manager = GoogleDriveManager()
        print("✅ Google Drive manager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Google Drive manager: {e}")
        print("This might be due to missing authentication or network issues")
        print("Google Drive features will be disabled")
        drive_manager = None
else:
    print("❌ credentials.json not found - Google Drive features disabled")

# Configure logging
logging.basicConfig(level=logging.INFO)


# Custom keyboard for better user experience
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📞 Share My Contact", request_contact=True))
    keyboard.add(KeyboardButton("💼 Portfolio"), KeyboardButton("🎨 Services"))
    keyboard.add(KeyboardButton("💰 Pricing"), KeyboardButton("📱 Social Media"))
    keyboard.add(KeyboardButton("🆘 Help"))
    return keyboard


def create_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📞 Share My Contact", request_contact=True))
    keyboard.add(KeyboardButton("↩️ Back to Main Menu"))
    return keyboard


# Welcome message handler
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message: Message):
    welcome_text = """
🎨 *Welcome to My Creative World!* 🎨

Hello there! I'm *Firaol*, your friendly graphic designer and digital artist. ✨

I'm absolutely thrilled to have you here! Whether you're looking to:
• Build an amazing brand identity
• Create stunning posters and flyers
• Design eye-catching digital art
• Or bring any creative vision to life

I'm here to help make it happen! 🌟

*Here's what you can do:*
📞 `/contact` - Share your contact info with me
💼 `/portfolio` - See my latest work
🎨 `/services` - Explore what I offer
💰 `/pricing` - Check my affordable rates
📱 `/social` - Connect with me on social media
🆘 `/help` - Get assistance

*Quick Tip:* You can also use the menu buttons below to navigate easily!

*Ready to create something amazing together?* 🚀
    """

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

    # Send a follow-up message with emojis
    bot.send_message(
        message.chat.id,
        "💫 *Let's bring your ideas to life!* \n\nDon't hesitate to reach out - I'm excited to work with you! 😊",
        parse_mode='Markdown'
    )


# Contact command - share Telegram contact
@bot.message_handler(commands=['contact'])
def contact_command(message: Message):
    contact_text = """
📞 *Let's Connect!*

Sharing your contact info helps me:
• Reach out to discuss your project
• Send you updates and previews
• Provide better customer service

*Simply tap the "Share My Contact" button below* 👇

Your privacy is important - I'll only use your contact for project-related communication. 🤝
    """

    bot.send_message(
        message.chat.id,
        contact_text,
        parse_mode='Markdown',
        reply_markup=create_contact_keyboard()
    )


# Handle shared contact information
@bot.message_handler(content_types=['contact'])
def handle_contact(message: Message):
    contact = message.contact
    user_info = f"""
✅ *New Contact Shared!*

👤 *Name:* {contact.first_name} {contact.last_name or ''}
📞 *Phone:* {contact.phone_number}
🆔 *User ID:* {contact.user_id}

*Thank you for sharing your contact!* 🙏

I'll reach out to you shortly to discuss how we can work together. In the meantime, feel free to browse my portfolio or check out my services!
    """

    # Send confirmation to user
    bot.send_message(
        message.chat.id,
        user_info,
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

    # Send notification to admin (you)
    admin_notification = f"""
📱 *NEW CONTACT RECEIVED*

👤 *From:* {contact.first_name} {contact.last_name or ''}
📞 *Phone:* {contact.phone_number}
🆔 *Telegram ID:* @{message.from_user.username or 'N/A'}
💬 *Username:* {message.from_user.first_name}

*Reach out and start a conversation!* 🚀
    """

    bot.send_message(CHAT_ID, admin_notification, parse_mode='Markdown')


# Portfolio command
@bot.message_handler(commands=['portfolio'])
def portfolio_command(message: Message):
    portfolio_text = """
🎨 *My Portfolio Highlights*

Here's a glimpse of my creative work:

✨ *Brand Identity & Logos*
• Complete brand packages
• Logo design & variations
• Business card designs

✨ *Posters & Flyers*
• Event promotions
• Concert posters
• Marketing materials

✨ *Digital Art*
• Custom illustrations
• Tech-themed artwork
• Creative compositions

✨ *Social Media Graphics*
• Instagram posts & stories
• Facebook covers
• Twitter headers

*Want to see more?* 
Visit my online portfolio or check out my Instagram: @firaolanbessaofficial 📱
    """

    bot.send_message(message.chat.id, portfolio_text, parse_mode='Markdown')


# Services command
@bot.message_handler(commands=['services'])
def services_command(message: Message):
    services_text = """
🛠️ *My Services*

I offer a wide range of design services:

🎯 *Branding & Identity*
• Logo Design
• Brand Guidelines
• Business Cards
• Letterheads

🎯 *Print Design*
• Posters & Flyers
• Brochures
• Magazine Layouts
• Product Packaging

🎯 *Digital Design*
• Social Media Graphics
• Web Banners
• Email Templates
• Presentation Designs

🎯 *Illustration*
• Custom Illustrations
• Character Design
• Digital Artwork
• Concept Art

*Don't see what you need?* 
Just ask! I'm always open to new challenges. 💪
    """

    bot.send_message(message.chat.id, services_text, parse_mode='Markdown')


# Pricing command
@bot.message_handler(commands=['pricing'])
def pricing_command(message: Message):
    pricing_text = """
💰 *Pricing Overview*

I believe in transparent, fair pricing:

🎨 *Logo Design*
• Negotiable
• Basic Logo: $50-$100
• Complete Brand Package: $150-$300

📄 *Poster/Flyer Design*
• Negotiable
• Single Design: $30-$60
• Multiple Variations: $80-$150

📱 *Social Media Package*
• Negotiable
• Monthly Package (10 posts): $200-$400
• Single Posts: $25 each

🖼️ *Custom Illustrations*
• Negotiable
• Simple Illustration: $50-$100
• Complex Artwork: $100-$250

*Note:* All prices are starting points. Final quotes depend on project complexity and requirements.

💡 *Ready to get a custom quote?*
Share your contact or send me a message with your project details!
    """

    bot.send_message(message.chat.id, pricing_text, parse_mode='Markdown')


# Social media command
@bot.message_handler(commands=['social'])
def social_command(message: Message):
    social_text = """
📱 *Let's Connect on Social Media!*

Follow me for daily inspiration and updates:

📸 *Instagram:* @firaolanbessaofficial
🎨 *Behance:* https://behance.net/firaoldebesa1
💼 *Dribbble:* https://dribbble.com/firanova
📱 *LinkedIn:* https://linkedin.com/in/firaolanbessaofficial

*Why follow me?*
• See my latest work
• Get design tips and tricks
• Be the first to know about special offers
• Join my creative community

I love connecting with fellow creatives and clients! 🤝
    """

    bot.send_message(message.chat.id, social_text, parse_mode='Markdown')


# Help command
@bot.message_handler(commands=['help'])
def help_command(message: Message):
    help_text = """
🆘 *How Can I Help You?*

Here are all the commands you can use:

/start - Welcome message and introduction
/contact - Share your contact information
/portfolio - View my design portfolio
/services - See all services I offer
/pricing - Check my pricing structure
/social - Find me on social media
/help - Show this help message

*Quick Actions:*
• Use the menu buttons for easy navigation
• Share your contact to start a project discussion
• Check my portfolio to see my style

*Having issues?*
If something isn't working or you have questions, just type your question and I'll help you out!

*Ready to create something amazing?* 🚀
    """

    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


# Handle text messages for button responses
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message: Message):
    text = message.text.lower()

    if text == '💼 portfolio':
        portfolio_command(message)
    elif text == '🎨 services':
        services_command(message)
    elif text == '💰 pricing':
        pricing_command(message)
    elif text == '📱 social media':
        social_command(message)
    elif text == '🆘 help':
        help_command(message)
    elif text == '↩️ back to main menu':
        bot.send_message(
            message.chat.id,
            "🏠 *Back to Main Menu*",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    else:
        # Friendly response for unrecognized messages
        bot.send_message(
            message.chat.id,
            "😊 I'm here to help! Use the commands or menu buttons to explore what I can do for you.\n\nTry /help to see all available options!",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )


# Flask routes for your website
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/images')
def api_images():
    """Return paginated images from both local storage and Google Drive."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 6))
    
    all_images = []
    
    # Get local images
    images_dir = os.path.join(app.static_folder, 'images')
    if os.path.isdir(images_dir):
        supported_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        for name in os.listdir(images_dir):
            ext = os.path.splitext(name)[1].lower()
            if ext in supported_exts:
                file_url = url_for('static', filename=f'images/{name}')
                base = os.path.splitext(name)[0]
                title = base.replace('_', ' ').replace('-', ' ').title()
                all_images.append({
                    'src': file_url,
                    'title': title,
                })
    
    # Get Google Drive images
    if drive_manager:
        try:
            drive_images = drive_manager.get_all_images()
            all_images.extend(drive_images)
        except Exception as e:
            print(f"Error fetching Google Drive images: {e}")
    
    # Calculate pagination
    total = len(all_images)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = all_images[start:end]
    
    return jsonify({
        'images': paginated_images,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    })


@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload image to Google Drive."""
    print("Upload endpoint hit!")
    
    print(f"Files: {request.files}")
    print(f"Form: {request.form}")
    
    if 'file' not in request.files:
        print("No file in request")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    title = request.form.get('title', 'Untitled')
    
    print(f"File: {file.filename}, Title: {title}")
    
    if file.filename == '':
        print("Empty filename")
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        print("Invalid file type")
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Try Google Drive first, fallback to local if not available
    if drive_manager is None:
        print("Google Drive manager not initialized - falling back to local storage")
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.static_folder, 'images', filename)
            file.save(filepath)
            
            file_url = url_for('static', filename=f'images/{filename}')
            return jsonify({
                'success': True, 
                'data': {
                    'url': file_url,
                    'title': title,
                    'source': 'local'
                }
            })
        except Exception as e:
            print(f"Local save failed: {e}")
            return jsonify({'error': 'Upload failed'}), 500
    
    # Google Drive upload
    try:
        print("Processing Google Drive upload...")
        
        # Read file into memory instead of saving to disk
        file_content = file.read()
        file.seek(0)  # Reset file pointer
        
        print(f"File size: {len(file_content)} bytes")
        
        # Upload to Drive using memory buffer
        result = drive_manager.upload_image_from_memory(file_content, file.filename, title)
        print(f"Drive upload result: {result}")
        
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'error': 'Upload failed'}), 500
            
    except Exception as e:
        print(f"Upload exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    email = request.form.get('email')
    project_type = request.form.get('project_type')
    description = request.form.get('description')

    print("New Order Received:")
    print("Name:", name)
    print("Email:", email)
    print("Project Type:", project_type)
    print("Description:", description)

    message = f"""
📩 *New Graphic Design Request*  
👤 *Name:* {name}  
📧 *Email:* {email}  
🎨 *Project Type:* {project_type}  
📝 *Description:*  
{description}
    """

    # Send message to your Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

    return render_template('thankyou.html')


def start_bot_polling():
    """Start the bot in polling mode"""
    try:
        print("🤖 Starting Telegram Bot in polling mode...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Bot polling error: {e}")
        # Restart polling after a delay
        import time
        time.sleep(5)
        start_bot_polling()


if __name__ == "__main__":
    # Start bot polling in a separate thread
    bot_thread = threading.Thread(target=start_bot_polling)
    bot_thread.daemon = True
    bot_thread.start()

    print("🚀 Bot started successfully!")
    print("💫 New features activated:")
    print("   - Warm welcome messages")
    print("   - Contact sharing")
    print("   - Interactive menus")
    print("   - Portfolio commands")
    print("   - Pricing information")

    # Start Flask app
    app.run("0.0.0.0", port=5000, debug=True)