from django.contrib import admin



from .models import Article,Comment

admin.site.register(Comment)

# Register your models here.
@admin.register(Article)
class AticleAdmin (admin.ModelAdmin):

    list_display = ["title","auther", "creded_date"]

    list_display_links = ["title","creded_date"]

    search_fields = ["title"]

    list_filter = ["creded_date"]
    class Meta: 
        model = Article

