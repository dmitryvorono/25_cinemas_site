from flask_app.flask_server import app
import os
from config import SITE_IP_ADDRESS, SITE_PORT

app.run(host=os.getenv('IP', SITE_IP_ADDRESS),
        port=int(os.getenv('PORT', SITE_PORT)))