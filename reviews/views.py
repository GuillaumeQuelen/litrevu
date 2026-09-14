from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows
from django.db.models import Q
from itertools import chain
from .forms import TicketForm, ReviewForm, FollowUserForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def flux(request):
    suivis = request.user.following.values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=suivis))
    reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=suivis))
    flux_items = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, 'reviews/flux.html', {'Flux': flux_items})

from .forms import TicketForm


@login_required
def create_ticket(request):
    form = TicketForm()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')

    return render(request, 'reviews/create_ticket.html', {'form': form})

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return redirect('flux')

    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')

    return render(request, 'reviews/update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return redirect('flux')

    if request.method == 'POST':
        ticket.delete()
        return redirect('flux')

    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')

    return render(request, 'reviews/create_review.html', {'form': form, 'ticket': ticket})

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect('flux')

    form = ReviewForm(instance=review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('flux')

    return render(request, 'reviews/update_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect('flux')

    if request.method == 'POST':
        review.delete()
        return redirect('flux')

    return render(request, 'reviews/delete_review.html', {'review': review})

@login_required
def follow_users(request):
    form = FollowUserForm()
    message = ''

    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)
            except User.DoesNotExist:
                message = "Cet utilisateur n'existe pas."
            else:
                if user_to_follow == request.user:
                    message = "Vous ne pouvez pas vous suivre vous-même."
                elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                    message = "Vous suivez déjà cet utilisateur."
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                    return redirect('follow_users')

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    return render(request, 'reviews/follow_users.html', {
        'form': form,
        'message': message,
        'following': following,
        'followers': followers,
    })

@login_required
def unfollow_user(request, follow_id):
    follow = get_object_or_404(UserFollows, id=follow_id)

    if follow.user != request.user:
        return redirect('follow_users')

    if request.method == 'POST':
        follow.delete()
        return redirect('follow_users')

    return render(request, 'reviews/unfollow_user.html', {'follow': follow})


@login_required
def create_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')

    return render(request, 'reviews/create_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form,
    })

@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    posts = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    return render(request, 'reviews/my_posts.html', {'posts': posts})