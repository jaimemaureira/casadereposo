# masterbikes/forms.py

from django import forms
from .models import Reserva, Reparacion, Feedback, Bicicleta
from django.utils import timezone
from datetime import timedelta


class BicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)

class ReservaForm(forms.ModelForm):
    fecha_entrega = forms.DateTimeField(
        initial=timezone.now() + timedelta(days=7),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Reserva
        fields = ['bicicleta', 'fecha_entrega']

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['bicicleta'].queryset = Bicicleta.objects.all()
        self.fields['bicicleta'].widget.attrs.update({'class': 'form-control'})

        # Adding data-image-url attribute to each option
        self.fields['bicicleta'].widget.choices = [(b.pk, b.nombre) for b in Bicicleta.objects.all()]
        for bicicleta in self.fields['bicicleta'].queryset:
            self.fields['bicicleta'].widget.attrs[f'data-image-url-{bicicleta.pk}'] = bicicleta.imagen.url

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data['fecha_entrega']
        if fecha_entrega > timezone.now() + timedelta(weeks=1):
            raise forms.ValidationError("La fecha de entrega no puede ser más de una semana a partir de hoy.")
        return fecha_entrega
    
class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['bicicleta', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReparacionForm, self).__init__(*args, **kwargs)
        self.fields['bicicleta'].queryset = Bicicleta.objects.all()
        self.fields['bicicleta'].widget.attrs.update({'class': 'form-control'})

        self.fields['bicicleta'].widget.choices = [(b.pk, b.nombre) for b in Bicicleta.objects.all()]
        for bicicleta in self.fields['bicicleta'].queryset:
            self.fields['bicicleta'].widget.attrs[f'data-image-url-{bicicleta.pk}'] = bicicleta.imagen.url

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario', 'calificacion']
