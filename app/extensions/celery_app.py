from celery import Celery

celery = Celery(__name__)

def init_celery(app):

    broker = app.config.get("CELERY_BROKER_URL") or app.config.get("broker_url")
    backend = app.config.get("CELERY_RESULT_BACKEND") or app.config.get("result_backend")

    if broker:
        celery.conf.broker_url = broker
    if backend:
        celery.conf.result_backend = backend


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery