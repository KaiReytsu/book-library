from django.contrib import admin

from . import models

'''
admin.site.register(models.Book)
admin.site.register(models.Reservation)
admin.site.register(models.Author)
admin.site.register(models.UserProfile)
'''
admin.site.register(models.Publisher)
admin.site.register(models.Genre)

admin.site.register(models.Language)

class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = models.Book


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration object for Author models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('author_name', 'date_of_birth', 'date_of_death')
    fields = ['author_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class ReservationInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = models.Reservation


class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('book_name', 'author', 'display_genre')
    inlines = [ReservationInline]


admin.site.register(models.Book, BookAdmin)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Administration object for BookInstance models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('book', 'status', 'user', 'date_of_issue', 'date_of_return')
    list_filter = ('status', 'date_of_issue', 'date_of_return')

    fieldsets = (
        ('Заголовок бронирования', {
            'fields': ('book', 'id')
        }),
        ('Информация', {
            'fields': ('status', 'date_of_issue', 'date_of_return', 'user')
        }),
    )