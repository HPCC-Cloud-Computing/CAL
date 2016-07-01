
#
# class Controller(object):
#     pass

def _load_pipeline(loader, pipeline):
    filters = [loader.get_filter(n) for n in pipeline[:-1]]
    app = loader.get_app(pipeline[-1])
    filters.reverse()
    for filter in filters:
        app = filter(app)
    return app

def pipeline_factory_v1(loader, global_conf, **local_conf):
    """A paste pipeline replica that keys off of auth_strategy."""
    # return _load_pipeline(loader, local_conf[CONF.auth_strategy].split())
    return _load_pipeline(loader, local_conf['default'].split())