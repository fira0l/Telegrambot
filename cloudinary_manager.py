import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url

class CloudinaryManager:
    def __init__(self):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        print("✅ Cloudinary configured successfully")
    
    def upload_image(self, file_content, filename, title):
        """Upload image to Cloudinary"""
        try:
            # Upload with transformation and metadata
            result = cloudinary.uploader.upload(
                file_content,
                public_id=f"portfolio/{filename.split('.')[0]}",
                folder="portfolio",
                resource_type="image",
                context=f"title={title}",
                transformation=[
                    {"quality": "auto", "fetch_format": "auto"}
                ]
            )
            
            return {
                'id': result['public_id'],
                'url': result['secure_url'],
                'title': title,
                'width': result.get('width'),
                'height': result.get('height')
            }
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return None
    
    def get_all_images(self):
        """Get all images from Cloudinary portfolio folder"""
        try:
            # Get all images from portfolio folder
            result = cloudinary.api.resources(
                type="upload",
                prefix="portfolio/",
                max_results=100,
                context=True
            )
            
            images = []
            for resource in result.get('resources', []):
                # Get optimized URL with HTTPS
                url = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/image/upload/c_fill,h_600,q_auto,w_800/{resource['public_id']}.jpg"
                
                # Extract title from context or filename
                title = resource.get('context', {}).get('custom', {}).get('title', 
                       resource['public_id'].split('/')[-1].replace('_', ' ').title())
                
                images.append({
                    'id': resource['public_id'],
                    'src': url,
                    'title': title,
                    'width': resource.get('width'),
                    'height': resource.get('height')
                })
            
            return images
        except Exception as e:
            print(f"Cloudinary fetch error: {e}")
            return []
    
    def delete_image(self, public_id):
        """Delete image from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            print(f"Cloudinary delete error: {e}")
            return False