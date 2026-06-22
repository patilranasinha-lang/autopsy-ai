from app import create_app, db
from flask_migrate import Migrate
import os

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
