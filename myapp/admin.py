from django.apps import apps
from django.contrib import admin

app = apps.get_app_config('myapp')
admin_classes = {
}
for model_name, model in app.models.items():
    if model in admin_classes:
        admin.site.register(model, admin_classes[model])
    else:
        admin.site.register(model)