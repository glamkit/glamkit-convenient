from django.db.models.signals import post_save

def post_save_handler(model):
    def renderer(func):
        post_save.connect(func, sender=model)
        return func
    return renderer

