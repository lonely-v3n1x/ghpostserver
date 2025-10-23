from wsgi import app

# Vercel handler for Flask app
def handler(environ, start_response):
    return app(environ, start_response)