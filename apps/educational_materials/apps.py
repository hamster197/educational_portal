from django.apps import AppConfig


class EducationalMaterialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.educational_materials"
    verbose_name = 'Образовательные материалы'

    def ready(self):
        import apps.educational_materials.signals
