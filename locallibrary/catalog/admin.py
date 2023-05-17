from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

#define the admin class
<<<<<<< HEAD

=======
class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields =['first_name','last_name',('date_of_birth', 'date_of_death')]

#register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
>>>>>>> 5d243dd (PrimerPush)

#register the admin classes for book using the decorator

#register the admin classes for bookinstances using the decorator
@admin.register(BookInstance)
class BookInstancesAdmin(admin.ModelAdmin):
    list_filter=('status','due_back')
<<<<<<< HEAD
    list_display=('book','status','borrower','due_back','imprint','id')

    fieldsets=(
        (None,{
            'fields':('book', 'imprint', 'id','borrower')
=======
    list_display=('book','status','due_back','imprint','id')

    fieldsets=(
        (None,{
            'fields':('book', 'imprint', 'id')
>>>>>>> 5d243dd (PrimerPush)
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
<<<<<<< HEAD

class BookInline(admin.TabularInline):
    model = Book
class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields =['first_name','last_name',('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

#register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
=======
>>>>>>> 5d243dd (PrimerPush)
