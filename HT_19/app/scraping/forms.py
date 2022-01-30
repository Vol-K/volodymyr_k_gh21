from django import forms


class CategoryForm(forms.Form):
    categories = (
        ('askstories', 'Askstories'),
        ('showstories', 'Showstories'),
        ('newstories', 'Newstories'),
        ('jobstories', 'Jobstories'),
    )
    
    field = forms.CharField(
        widget=forms.Select(choices=categories)
    )
