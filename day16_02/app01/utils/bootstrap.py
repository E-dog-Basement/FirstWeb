from django import forms


class BootStrapModelForm(forms.ModelForm):
    exclude_field = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in self.exclude_field:
                continue
            field.widget.attrs['class'] = 'form-control'