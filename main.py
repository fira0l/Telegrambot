
from flask import Flask, request, render_template
import logging
import requests

app = Flask(__name__)

import telebot


bot = telebot.TeleBot(token)


from telebot.types import Message


    
    
@bot.message_handler(commands=['start','hello'])
def start(message: Message):
    bot.send_message(message.chat.id, "Hello! I'm your bot. How can I assist you today?")
    # You can add more functionality here, like showing a menu or options.
    
    
@bot.message_handler(commands=['help'])
def help_command(message: Message):
    bot.send_message(message.chat.id, "Here are some commands you can use:\n/start - Start the bot\n/help - Show this help message")
    # You can add more commands and their descriptions here.    

@bot.message_handler(func=lambda message: True)
def echo_all(message: Message):
    bot.reply_to(message, message.text)
    # This will echo back any message sent to the bot. You can customize this behavior.
    
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')

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


    
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     json_str = request.get_data().decode('UTF-8')
#     update = telebot.types.Update.de_json(json_str)
#     bot.process_new_updates([update])
#     return '!', 200

# @app.route('/set_webhook', methods=['GET', 'POST'])
# def set_webhook():
#     s = bot.set_webhook(url='https://localhost:8080/webhook')
#     if s:
#         return "Webhook set successfully!", 200
#     else:
#         return "Failed to set webhook.", 400
    
# @app.route('/delete_webhook', methods=['GET', 'POST'])
# def delete_webhook():
#     bot.delete_webhook()
#     return "Webhook deleted successfully!", 200

# @app.route('/')
# def index():
#     return "Hello, this is the webhook server!"

# @app.route('/start', methods=['GET'])
# def start_webhook():
#     return "Webhook started!"
    
if __name__ == "__main__":
    # Start the bot polling
    try:
        print("Bot is running...")
        # bot.polling(none_stop=True)
        app.run("0.0.0.0", port=8080, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you can add logging or error handling here.