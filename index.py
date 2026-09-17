from app import app, handler

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import os
    port = int(os.environ.get('PORT', 8080))
    print(f"Serving dashboard on http://localhost:{port}")
    with make_server('', port, app) as httpd:
        httpd.serve_forever()
