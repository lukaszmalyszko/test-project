from flask_celery import FlaskCelery


def make_app(tasks_module):
    app = FlaskCelery(include=[tasks_module])
    default_commands = f"tasks"
    app.conf.task_default_queue = default_commands
    return app


app = make_app("project.worker.handlers")
