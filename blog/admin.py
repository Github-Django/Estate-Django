from django.contrib import admin
from .models import Article, Category
from .models import PostImage


class PostImageAdmin(admin.TabularInline):
    model = PostImage
    extra = 3

    class Meta:
        model = Article


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "author":
    #         kwargs['queryset'] = MyUser.objects.filter(is_staff=True)
    #         return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = (
        'title', 'author', 'jpublish', 'property_contract', 'property_type', 'unit_price', 'category_to_str', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    ordering = ('-publish', '-status')
    prepopulated_fields = {'slug': ('title',)}  # title va slug ba ham set mishan
    inlines = [PostImageAdmin]




# Register your models here.
admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}  # title va slug ba ham set mishan


admin.site.register(Category, CategoryAdmin)
