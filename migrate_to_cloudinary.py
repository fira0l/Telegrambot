import os
from cloudinary_manager import CloudinaryManager
from dotenv import load_dotenv

def migrate_local_images():
    """Migrate all local images to Cloudinary"""
    load_dotenv()
    
    try:
        cloudinary_manager = CloudinaryManager()
        print("✅ Cloudinary initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Cloudinary: {e}")
        return
    
    images_dir = "static/images"
    if not os.path.isdir(images_dir):
        print(f"❌ Images directory not found: {images_dir}")
        return
    
    supported_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    uploaded_count = 0
    failed_count = 0
    
    print(f"📁 Scanning {images_dir} for images...")
    
    for filename in os.listdir(images_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_exts:
            continue
            
        filepath = os.path.join(images_dir, filename)
        title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
        
        print(f"📤 Uploading: {filename} -> {title}")
        
        try:
            with open(filepath, 'rb') as f:
                file_content = f.read()
            
            result = cloudinary_manager.upload_image(file_content, filename, title)
            
            if result:
                print(f"✅ Uploaded: {title} -> {result['url']}")
                uploaded_count += 1
            else:
                print(f"❌ Failed to upload: {filename}")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error uploading {filename}: {e}")
            failed_count += 1
    
    print(f"\n📊 Migration Summary:")
    print(f"✅ Successfully uploaded: {uploaded_count}")
    print(f"❌ Failed uploads: {failed_count}")
    print(f"🎉 Migration complete!")

if __name__ == "__main__":
    migrate_local_images()