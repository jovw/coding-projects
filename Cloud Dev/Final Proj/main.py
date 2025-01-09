from app import create_app
import uuid

app = create_app()

if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.run(host='127.0.0.1', port=8080, debug=True)
