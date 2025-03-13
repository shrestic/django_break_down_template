import os
from werkzeug.serving import run_simple
from django.core.wsgi import get_wsgi_application

# Thiết lập DJANGO_SETTINGS_MODULE trước
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainkode_example.settings")

application = get_wsgi_application()

if __name__ == "__main__":
    run_simple("0.0.0.0", 8001, application, use_reloader=True, use_debugger=True)
