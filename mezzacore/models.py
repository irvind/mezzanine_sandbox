from django.db import models


class Permissions(models.Model):

    class Meta:
        managed = True
        permissions = (
            ('view_drafts', 'Просмотр черновиков'),
            ('make_public_drafts', 'Публикация черновиков на сайт'),
            ('change_seo', 'Управление требованиями SEO'),
            ('change_lang', 'Управление мультиязычностью'),
        )
        default_permissions = ()
