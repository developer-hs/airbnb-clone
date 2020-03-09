from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    Check_in = forms.IntegerField(max_value=5, min_value=1)
    Accuracy = forms.IntegerField(max_value=5, min_value=1)
    Location = forms.IntegerField(max_value=5, min_value=1)
    Cleanliness = forms.IntegerField(max_value=5, min_value=1)
    Value = forms.IntegerField(max_value=5, min_value=1)
    Communication = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "reviews",
            "Check_in",
            "Accuracy",
            "Location",
            "Cleanliness",
            "Value",
            "Communication",
        )

    def save(self):
        review = super().save(commit=False)
        return review
