from flask import Flask, render_template, url_for
import datetime
import os
import random
from dotenv import load_dotenv

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')

load_dotenv()

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def asset_url(filename):
    """Return a static asset URL with a cache-busting version query."""

    file_path = os.path.join(app.static_folder, filename)
    version = int(os.path.getmtime(file_path)) if os.path.exists(file_path) else 0
    return url_for("static", filename=filename, v=version)


@app.context_processor
def inject_asset_url():
    return {"asset_url": asset_url}


def load_featured_images():
    """Return local images from static/images that are safe to display."""

    images_dir = os.path.join(app.static_folder, "images")
    if not os.path.isdir(images_dir):
        return []

    featured_images = []
    for filename in os.listdir(images_dir):
        file_path = os.path.join(images_dir, filename)
        _, extension = os.path.splitext(filename)
        if not os.path.isfile(file_path) or extension.lower() not in IMAGE_EXTENSIONS:
            continue

        label = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").strip()
        featured_images.append(
            {
                "image_url": asset_url(f"images/{filename}"),
                "alt": label or "Featured image",
                "caption_short": label.upper() or "RANDOM FEATURED IMAGE",
            }
        )

    return featured_images


def pick_featured_post():
    """Select a random local image for the homepage."""

    featured_posts = load_featured_images()
    if not featured_posts:
        return None

    return random.choice(featured_posts)

@app.route('/')
def home():
    """Render the main under construction page."""

    user_email = os.getenv('USER_EMAIL', '#')
    url_inst = os.getenv('URL_INSTAGRAM', '#')
    url_blog = os.getenv('URL_BLOG', '#')
    url_yt = os.getenv('URL_YOUTUBE', '#')
    url_flickr = os.getenv('URL_FLICKR', '#')

    user_data = {
        'email': user_email,
        'social_links': [
            {'name': 'Instagram', 'url': url_inst},
            {'name': 'Blog', 'url': url_blog},
            {'name': 'YT', 'url': url_yt},
            {'name': 'Flickr', 'url': url_flickr},
        ],
        'featured_images': load_featured_images(),
        'featured_post': pick_featured_post(),
        'current_year': datetime.datetime.today().year
    }
    return render_template('base.html', **user_data)

if __name__ == '__main__':
    app.run(debug=True)
