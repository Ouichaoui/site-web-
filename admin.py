from django.contrib import admin
from .models import *
# Register your models here
admin.site.register(Customer)
admin.site.register(Catalogue)
admin.site.register(ConversationMessage)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Offre)