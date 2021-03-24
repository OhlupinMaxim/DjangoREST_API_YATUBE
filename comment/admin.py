from django.contrib import admin

from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "author",
        "pub_date",
        "text"
    )


admin.site.register(Comment, CommentAdmin)
