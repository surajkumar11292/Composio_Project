import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler

# Standard WSGI entrypoint for Vercel Python Runtime
def app(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    root_dir = Path(__file__).parent
    
    if path in ('', '/', '/dashboard', '/dashboard/'):
        target = root_dir / 'dashboard' / 'index.html'
    else:
        clean = path.lstrip('/')
        target = root_dir / 'dashboard' / clean
        if not target.is_file():
            target = root_dir / clean
        if not target.is_file():
            target = root_dir / 'dashboard' / 'index.html'

    ext = target.suffix.lower()
    mime = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.webp': 'image/webp'
    }.get(ext, 'text/html; charset=utf-8')

    try:
        body = target.read_bytes()
        start_response('200 OK', [
            ('Content-Type', mime),
            ('Content-Length', str(len(body))),
            ('Cache-Control', 'public, max-age=0, must-revalidate')
        ])
        return [body]
    except Exception as e:
        err = f"Error: {e}".encode('utf-8')
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [err]

# Fallback BaseHTTPRequestHandler for Vercel Functions
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = Path(__file__).parent / 'dashboard' / 'index.html'
        if not target.is_file():
            target = Path(__file__).parent / 'index.html'
        body = target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = int(os.environ.get('PORT', 8080))
    print(f"Serving dashboard on http://localhost:{port}")
    with make_server('', port, app) as httpd:
        httpd.serve_forever()
