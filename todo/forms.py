from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):

    completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_completed',
        }),
        label='Marquer comme complétée'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'due_time']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le titre de la tâche',
                'maxlength': '200',
                'required': True,
                'id': 'id_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez une description détaillée (optionnel)',
                'rows': 5,
                'id': 'id_description',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_due_date',
            }),
            'due_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'id_due_time',
            }),
        }

        labels = {
            'title': 'Titre *',
            'description': 'Description',
            'due_date': 'Date d\'échéance',
            'due_time': 'Heure d\'échéance',
        }



        error_messages = {
            'title': {
                'required': 'Le titre est obligatoire.',
                'max_length': 'Le titre ne peut pas dépasser 200 caractères.',
            },
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        if self.instance and self.instance.pk:
            self.fields['completed'].initial = self.instance.is_completed

    def clean_title(self):

        title = self.cleaned_data.get('title')

        if title:

            title = title.strip()

            # Vérifier la longueur minimale
            if len(title) < 3:
                raise ValidationError('Le titre doit contenir au moins 3 caractères.')

            # Vérifier que le titre n'est pas vide après suppression des espaces
            if not title:
                raise ValidationError('Le titre ne peut pas être vide.')

        return title

    def clean_due_date(self):

        due_date = self.cleaned_data.get('due_date')
        return due_date

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        due_time = cleaned_data.get('due_time')

        # Si une heure est fournie sans date
        if due_time and not due_date:
            raise ValidationError({
                'due_time': 'Vous devez spécifier une date d\'échéance si vous ajoutez une heure.'
            })

        # Si date et heure sont fournies, vérifier que ce n'est pas dans le passé
        if due_date and due_time and not self.instance.pk:
            from datetime import datetime
            due_datetime = timezone.make_aware(
                datetime.combine(due_date, due_time)
            )
            if due_datetime < timezone.now():
                raise ValidationError({
                    'due_time': 'La date et l\'heure d\'échéance ne peuvent pas être dans le passé.'
                })

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Mettre à jour le bon attribut selon le modèle
        completed_value = self.cleaned_data.get('completed', False)
        if hasattr(instance, 'completed'):
            instance.completed = completed_value
        elif hasattr(instance, 'is_completed'):
            instance.is_completed = completed_value

        if commit:
            instance.save()
        return instance


class TaskFilterForm(forms.Form):
    #Formulaire de filtrage pour la liste des tâches

    STATUS_CHOICES = [
        ('all', 'Toutes'),
        ('pending', 'En attente'),
        ('completed', 'Complétées'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'filter_status',
        }),
        label='Statut'
    )