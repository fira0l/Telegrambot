# 🚀 Cyber Design Portfolio

![Cyber Design](https://img.shields.io/badge/Design-Cyberpunk-00f3ff?style=for-the-badge&logo=adobexd&logoColor=white)
![Flask](https://img.shields.io/badge/Built%20with-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Responsive](https://img.shields.io/badge/Responsive-Yes-00e6a1?style=for-the-badge&logo=web&logoColor=white)

> **Where Creativity Meets the Digital Frontier** - A cutting-edge graphic design portfolio built with cyberpunk aesthetics and modern web technologies.

---

## 👁️ **FOR CLIENTS** - View My Work & Order Services

### 🎨 **What I Offer**

I specialize in creating stunning visual designs that blend creativity with technology:

- **Logo Design & Brand Identity**
- **Poster & Flyer Design** 
- **Digital Art & Illustrations**
- **Event Marketing Materials**
- **Tech-Themed Graphics**

### 🖼️ **View My Portfolio**
Browse through my gallery of work featuring:
- Brand identities for businesses
- Event posters and flyers
- Digital artwork collections
- Motorsport and tech-themed designs

### 💼 **How to Order**

1. **Scroll down** to the "Initiate Project" section
2. **Fill out the form** with your project details
3. **Click "Transmit Request"** to send your project brief
4. **I'll contact you** within 24 hours to discuss your vision!

### 📞 **Get in Touch**
- **Instagram**: [@firaolanbessaofficial](https://www.instagram.com/firaolanbessaofficial)
- **Email**: [firaforpython@gmail.com]
- **Portfolio**: [Cyber Design Graphics Portfolio](https://telegrambot-48lt.onrender.com)

---

## ⚡ **FOR DEVELOPERS** - Technical Documentation

### 🛠️ **Tech Stack**

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom Cyberpunk CSS with animations
- **Fonts**: Rajdhani, Orbitron (Google Fonts)
- **Icons**: Custom CSS icons and emojis

### 🚀 **Features**

#### Design & UI
- ✅ **Cyberpunk Aesthetic** with neon colors and glows
- ✅ **Responsive Design** for all devices
- ✅ **Smooth Animations** and hover effects
- ✅ **Interactive Lightbox** for image viewing
- ✅ **Particle Effects** on click interactions
- ✅ **Glass Morphism** effects with backdrop blur

#### Functionality
- ✅ **Image Gallery** with modal lightbox
- ✅ **Navigation** between images with keyboard support
- ✅ **Contact Form** with validation
- ✅ **Mobile-Optimized** touch interactions
- ✅ **Performance Optimized** with lazy loading

### 📁 **Project Structure**
graphic-design-portfolio/
 * ├── static/
 * │ ├── css/
 * │ │ └── style.css # Main cyberpunk styles
 * │ └── images/
 * │ ├── abeni's burger.jpg
 * │ ├── 7639.jpg
 * │ └── ... (all portfolio images)
 * ├── templates/
 * │ └── index.html # Main portfolio page
 * ├── main.py # Flask application
 * ├── requirements.txt # Python dependencies
 * └── README.md


### 🏃 **Quick Start**

1. **Clone the repository**
   ```bash
   git clone https://github.com/fira0l/Telegrambot.git
   cd Telegrambot
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python main.py
   ```
4. **View in browser**
   ```bash
   http://localhost:5000
   ```
### ⚙️ **Configuration** 
#### Environment Variables

- Create a .env file for configuration:
```env
token=your_telegram_bot_token
CHAT_ID=your_chat_id
```

#### Flask App (main.py)
```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    # Process form data here
    name = request.form['name']
    email = request.form['email']
    project_type = request.form['project_type']
    description = request.form['description']
    
    # Add your email sending logic here
    print(f"New order from: {name} ({email})")
    print(f"Project: {project_type}")
    print(f"Details: {description}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

#### Requirements.txt

```txt
flask
telebot
requests
python-dotenv
```

### 🎨 **Customization Guide**
#### Colors (CSS Variables)

```css
:root {
    --neon-cyan: #00f3ff;
    --neon-purple: #b967ff;
    --neon-pink: #ff2a6d;
    --dark-bg: #0a0a16;
    --darker-bg: #050510;
}
```

#### Adding New Portfolio Items

1. Add images to static/images/
2. Update the gallery in index.html

```html
<div class="gallery-item" 
     data-image="{{ url_for('static', filename='images/your-image.jpg') }}" 
     data-title="YOUR_PROJECT_TITLE">
    <img src="{{ url_for('static', filename='images/your-image.jpg') }}" alt="Description">
    <div class="overlay">
        <h3>YOUR_PROJECT_TITLE</h3>
    </div>
</div>
```

### 🎯 **Browser Support**

* ✅ Chrome 90+
* ✅ Firefox 88+
* ✅ Safari 14+
* ✅ Edge 90+

### 📱 **Responsive Breakpoints**

* Mobile: < 768px
* Tablet: 768px - 1024px
* Desktop: > 1024px

### 🌟 **Special Features**

### Cyberpunk Elements

* Neon glow effects and gradients
* Scanline animations on hover
* Glitch text effects
* Particle system for interactions
* Cyber-style typography

### User Experience

* Keyboard navigation (ESC, Arrow keys)
* Smooth scrolling and transitions
* Loading states for images
* Accessible color contrasts

### 📞 **Support & Contact**

### For Clients

* Design Inquiries: [firaforpython@gmail.com]
* Portfolio: [Cyber Design Graphics Portfolio](https://telegrambot-48lt.onrender.com)
* Social: [Instagram @firaolanbessaofficial]

### For Developers

* Issues: GitHub Issues
* Pull Requests: Welcome!
* License: MIT

### 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
Built with ❤️ and neon lights
"Where creativity meets the digital frontier"
⬆ Back to Top
</div> 
