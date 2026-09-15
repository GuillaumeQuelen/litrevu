from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Q, Value
from django.shortcuts import get_object_or_404, redirect, render
from .forms import FollowUserForm, ReviewForm, TicketForm
from .models import Review, Ticket, UserBlocks, UserFollows
User = get_user_model()


@login_required
def flux(request):
    suivis = request.user.following.values_list('followed_user', flat=True)
    bloques = request.user.blocking.values_list('blocked_user', flat=True)
    bloquants = request.user.blocked_by.values_list('user', flat=True)

    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=suivis)
    ).exclude(
        Q(user__in=bloques) | Q(user__in=bloquants)
    ).annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.filter(
        Q(user=request.user)
        | Q(user__in=suivis)
        | Q(ticket__user=request.user)
    ).exclude(
        Q(user__in=bloques) | Q(user__in=bloquants)
    ).annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    tickets_critiques = Review.objects.filter(
        user=request.user
    ).values_list('ticket_id', flat=True)

    return render(request, 'reviews/flux.html', {
        'posts': posts,
        'tickets_critiques': tickets_critiques,
    })


@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value('TICKET', CharField())
    )
    reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value('REVIEW', CharField())
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'reviews/my_posts.html', {'posts': posts})


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

    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect('flux')

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
                elif UserBlocks.objects.filter(
                    Q(user=request.user, blocked_user=user_to_follow)
                    | Q(user=user_to_follow, blocked_user=request.user)
                ).exists():
                    message = "Impossible de suivre cet utilisateur."
                elif UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_follow
                ).exists():
                    message = "Vous suivez déjà cet utilisateur."
                else:
                    UserFollows.objects.create(
                        user=request.user, followed_user=user_to_follow
                    )
                    return redirect('follow_users')

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    blocks = UserBlocks.objects.filter(user=request.user)

    return render(request, 'reviews/follow_users.html', {
        'form': form,
        'message': message,
        'following': following,
        'followers': followers,
        'blocks': blocks,
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
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)

    if user_to_block == request.user:
        return redirect('follow_users')

    if request.method == 'POST':
        UserFollows.objects.filter(
            user=request.user, followed_user=user_to_block
        ).delete()
        UserFollows.objects.filter(
            user=user_to_block, followed_user=request.user
        ).delete()

        UserBlocks.objects.get_or_create(
            user=request.user, blocked_user=user_to_block
        )
        return redirect('follow_users')

    return render(request, 'reviews/block_user.html', {'user_to_block': user_to_block})


@login_required
def unblock_user(request, block_id):
    block = get_object_or_404(UserBlocks, id=block_id)

    if block.user != request.user:
        return redirect('follow_users')

    if request.method == 'POST':
        block.delete()
        return redirect('follow_users')

    return render(request, 'reviews/unblock_user.html', {'block': block})
