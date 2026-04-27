from flask import Flask, render_template
import os, datetime
from dotenv import load_dotenv  # Add this import

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')

# Load environment variables from .env file
load_dotenv()

@app.route('/')
def home():
    """Render the main under construction page."""

    # Read email from .env file or use placeholder
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
        'current_year': datetime.datetime.today().year
    }
    return render_template('base.html', **user_data)

if __name__ == '__main__':
    app.run(debug=True)