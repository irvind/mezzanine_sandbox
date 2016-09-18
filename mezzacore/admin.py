from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.sites.models import Site

from mezzanine.core.admin import SitePermissionUserAdmin
from mezzanine.core.models import SitePermission


class MyUserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if not email.endswith('bia-tech.ru'):
            raise forms.ValidationError('Неверный домен')

        return email

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.username = user.email
        user.is_staff, user.is_active = True, True

        password = get_random_string()
        user.set_password(password)

        message = 'Ваш логин: {}\nВаш пароль: {}'.format(user.username, password)
        user.email_user('Доступ к сайту БИА', message, 'noreply@bia-tech.ru')

        # Если форма сейвится из админки (она пока только там и есть), то commit == False
        if commit:
            user.save()

        return user


class MyUserAdmin(SitePermissionUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )
    add_form = MyUserCreationForm

    def save_related(self, request, form, formsets, change):
        """
        Даем права для всех сайтов.
        """
        # Сохраняем тут, т.к. в MyUserCreationForm.save() не можем
        user = form.instance
        perm, _ = SitePermission.objects.get_or_create(user=user)
        perm.sites.add(*Site.objects.all())

        return super(MyUserAdmin, self).save_related(request, form, formsets, change)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
