"""
  AuShadhaUser Admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import AuShadhaUser


class AuShadhaUserInline(admin.StackedInline):
    model = AuShadhaUser


class AuShadhaUserCreationForm(ModelForm):

    class Meta:
        #model = AuShadhaUser
        fields = [x.name for x in AuShadhaUser._meta.fields if x.name != 'id']
        exclude = []

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AuShadhaUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AuShadhaUserAdmin(admin.ModelAdmin):
    #model = AuShadhaUser
    pass

#class AuShadhaUserAdmin(UserAdmin):
    #inlines  = [ AuShadhaUserInline ]
#    extra = 2
#    add_form = AuShadhaUserCreationForm
#    change_form = AuShadhaUserCreationForm

    # fieldsets = (
        #(None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        #)

#    add_fieldsets = (
#        (None,
#         {'classes': ('wide',),
#          'fields': ('username',
#                     'email',
#                     'password',
#                     'first_name',
#                     'last_name',
#                     'is_superuser',
#                     'is_staff',
#                     'is_active',
#                     'last_login',
#                     'date_joined',
#                     'groups',
#                     'user_permissions',
#                     'aushadha_user_role'
#                     )
#          }
#         ),
#    )

#    change_fieldsets = (
#        (None,
#         {'classes': ('wide',),
#          'fields': ('username',
#                     'email',
#                     'password',
#                     'first_name',
#                     'last_name',
#                     'is_superuser',
#                     'is_staff',
#                     'is_active',
#                     'last_login',
#                     'date_joined',
#                     'groups',
#                     'user_permissions',
#                     'aushadha_user_role'
#                     )
#          }
#         ),
#    )

admin.site.register(AuShadhaUser, AuShadhaUserAdmin)
