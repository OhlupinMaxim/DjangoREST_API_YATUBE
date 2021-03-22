from django.contrib import admin

from review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
