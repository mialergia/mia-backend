from django.contrib import admin
from .models import TerminosCondiciones
from django import forms


class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TerminosCondiciones
        widgets = {
            'texto': forms.Textarea(attrs={'cols': 120, 'rows': 30}),
        }
        fields = '__all__'


class TerminosCondicionesAdmin(admin.ModelAdmin):
    form = TermsAndConditionsForm


admin.site.register(TerminosCondiciones, TerminosCondicionesAdmin)
