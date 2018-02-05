from flask_app.flask_server import app
import os
from config import site_ip_address, site_port

app.run(host=os.getenv('IP', site_ip_address),
        port=int(os.getenv('PORT', site_port)))