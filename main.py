import os
from flask import Flask, request, render_template
import logging
import requests
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import telebot
import threading
from flask import jsonify, url_for
from flask_cors import CORS
from google_drive import GoogleDriveManager
from cloudinary_manager import CloudinaryManager
from werkzeug.utils import secure_filename
import tempfile
import json


# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for Vercel frontend and localhost
CORS(app, origins=[
    'https://graphicdesign-pink.vercel.app',
    'http://localhost:5173',
    'http://localhost:3000'
])

# Get environment variables
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("token") or "dummy_token"
CHAT_ID = os.environ.get("CHAT_ID") or "dummy_chat_id"

# Initialize Telegram bot
bot = telebot.TeleBot(token)

# Initialize Cloudinary
cloudinary_manager = None
try:
    cloudinary_manager = CloudinaryManager()
except Exception as e:
    print(f"❌ Failed to initialize Cloudinary: {e}")
    cloudinary_manager = None

# Initialize Google Drive (fallback)
drive_manager = None
if not cloudinary_manager and os.path.exists('credentials.json'):
    try:
        print("Initializing Google Drive as fallback...")
        drive_manager = GoogleDriveManager()
        print("✅ Google Drive manager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Google Drive manager: {e}")
        drive_manager = None

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
    # Redirect to Vercel frontend
    return f'<script>window.location.href="https://graphicdesign-pink.vercel.app"</script>'

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Backend is running'}

@app.route('/migrate-images')
def migrate_images():
    """Migrate local images to Cloudinary"""
    if not cloudinary_manager:
        return jsonify({'error': 'Cloudinary not configured'}), 500
    
    try:
        from migrate_to_cloudinary import migrate_local_images
        migrate_local_images()
        return jsonify({'success': True, 'message': 'Migration completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/images')
def api_images():
    """Return paginated images from both local storage and Google Drive."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 6))
    
    print(f"API Images called: page={page}, per_page={per_page}")
    
    all_images = []
    
    # Get Cloudinary images (primary source)
    if cloudinary_manager:
        try:
            cloudinary_images = cloudinary_manager.get_all_images()
            all_images.extend(cloudinary_images)
            print(f"Loaded {len(cloudinary_images)} images from Cloudinary")
        except Exception as e:
            print(f"Error fetching Cloudinary images: {e}")
    
    # Fallback to local images if Cloudinary not available
    if not cloudinary_manager or len(all_images) == 0:
        print("Loading local images as fallback...")
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
            print(f"Loaded {len(all_images)} local images as fallback")
    
    # Calculate pagination
    total = len(all_images)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = all_images[start:end]
    
    print(f"Returning {len(paginated_images)} images for page {page}")
    
    response = {
        'images': paginated_images,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }
    
    print(f"API Response: {response}")
    return jsonify(response)


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
    
    # Try Cloudinary first
    if cloudinary_manager:
        try:
            print("Processing Cloudinary upload...")
            
            # Read file into memory
            file_content = file.read()
            print(f"File size: {len(file_content)} bytes")
            
            # Upload to Cloudinary
            result = cloudinary_manager.upload_image(file_content, file.filename, title)
            print(f"Cloudinary upload result: {result}")
            
            if result:
                return jsonify({'success': True, 'data': result})
            else:
                return jsonify({'error': 'Cloudinary upload failed'}), 500
                
        except Exception as e:
            print(f"Cloudinary upload exception: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    
    # Fallback to local storage
    print("Cloudinary not available - falling back to local storage")
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

    # Redirect back to Vercel frontend with success message
    return f'<script>window.location.href="https://graphicdesign-pink.vercel.app?success=true"</script>'


def start_bot_polling():
    """Start the bot in polling mode with conflict handling"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"🤖 Starting Telegram Bot (attempt {retry_count + 1})...")
            bot.polling(none_stop=True, interval=0, timeout=20)
            break
        except Exception as e:
            retry_count += 1
            print(f"❌ Bot error (attempt {retry_count}): {e}")
            if "409" in str(e) or "Conflict" in str(e):
                print("Bot conflict - another instance running")
                if retry_count < max_retries:
                    print(f"Waiting 30 seconds...")
                    import time
                    time.sleep(30)
                else:
                    print("Max retries reached - bot offline, Flask continues")
                    break
            else:
                import time
                time.sleep(5)


if __name__ == "__main__":
    # Start bot polling in a separate thread with error isolation
    def start_bot_safe():
        try:
            start_bot_polling()
        except Exception as e:
            print(f"Bot thread error (Flask continues): {e}")
    
    bot_thread = threading.Thread(target=start_bot_safe)
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
    port = int(os.environ.get("PORT", 5000))
    app.run("0.0.0.0", port=port, debug=False)