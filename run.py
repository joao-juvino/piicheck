from app import create_app
from app.extensions.celery_app import init_celery, celery

app = create_app()
init_celery(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)