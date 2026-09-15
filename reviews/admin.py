from django.contrib import admin
from .models import Ticket, Review, UserFollows, UserBlocks

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
admin.site.register(UserBlocks)
