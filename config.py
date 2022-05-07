import os
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.environ.get('EMAIL', None)
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', None)
