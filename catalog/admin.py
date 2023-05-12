from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

#define the admin class


#register the admin classes for book using the decorator

#register the admin classes for bookinstances using the decorator
@admin.register(BookInstance)
class BookInstancesAdmin(admin.ModelAdmin):
    list_filter=('status','due_back')
    list_display=('book','status','borrower','due_back','imprint','id')

    fieldsets=(
        (None,{
            'fields':('book', 'imprint', 'id','borrower')
        }),
        ('Availability',{
            'fields':('status', 'due_back')
        }),
    )

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','display_genre','language')
    
    inlines = [BookInstanceInline]

class BookInline(admin.TabularInline):
    model = Book
class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields =['first_name','last_name',('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

#register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)