from django import forms
from .models import Ticket, Review
from django.contrib.auth import get_user_model

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label='Note'
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

User = get_user_model()

class FollowUserForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')