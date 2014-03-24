from django.contrib import admin
from mysite.forum.models import Categories, Subcategories, Topics, Messages

admin.site.register(Categories)
admin.site.register(Subcategories)
admin.site.register(Topics)
admin.site.register(Messages)