from dynaconf import FlaskDynaconf


def init_app(app, **config):
    FlaskDynaconf(app, **config)
    if config:
        app.config.update(config)