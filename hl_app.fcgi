#!/home/richysix/python/python3.12/bin/python3
from flup.server.fcgi import WSGIServer
from app import create_app

app = create_app()

if __name__ == '__main__':
    WSGIServer(app).run()
