import os
from flask import Flask, jsonify, url_for, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])

@app.route('/api/images')
def api_images():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 6))
    
    print(f"API Images called: page={page}, per_page={per_page}")
    
    all_images = []
    
    # Get local images
    images_dir = os.path.join(app.static_folder, 'images')
    print(f"Images directory: {images_dir}")
    print(f"Directory exists: {os.path.isdir(images_dir)}")
    
    if os.path.isdir(images_dir):
        supported_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        files = os.listdir(images_dir)
        print(f"Found {len(files)} files in directory")
        
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in supported_exts:
                file_url = url_for('static', filename=f'images/{name}')
                base = os.path.splitext(name)[0]
                title = base.replace('_', ' ').replace('-', ' ').title()
                all_images.append({
                    'src': file_url,
                    'title': title,
                })
                print(f"Added image: {title} -> {file_url}")
    
    print(f"Total images found: {len(all_images)}")
    
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

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)