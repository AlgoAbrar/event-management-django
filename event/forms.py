from django import forms
from .models import Event, Participant, Category

class StyledFormMixin:
    
    default_classes = (
        # "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        # "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.TextInput):
                widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5,
                })
            elif isinstance(widget, (forms.SelectDateWidget, forms.DateInput)):
                widget.attrs.update({
                    "class": self.default_classes,
                    "type": "date",
                })
            elif isinstance(widget, forms.TimeInput):
                widget.attrs.update({
                    "class": self.default_classes,
                    "type": "time",
                })
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update({
                    'class': "space-y-2",
                })
            elif isinstance(widget, forms.Select):
                widget.attrs.update({
                    'class': self.default_classes,
                })
            else:
                widget.attrs.update({
                    'class': self.default_classes,
                })



class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants']
        widgets = {
            'description': forms.Textarea,
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'participants': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class ParticipantForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
