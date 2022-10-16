from datetime import datetime, timedelta

from django.contrib import admin

from . import models

"""
admin.site.register(models.Book)
admin.site.register(models.Reservation)
admin.site.register(models.Author)
admin.site.register(models.UserProfile)
"""
admin.site.register(models.Publisher)
admin.site.register(models.Genre)

admin.site.register(models.Language)


class BooksInline(admin.TabularInline):

    model = models.Book


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("author_name", "date_of_birth", "date_of_death")
    fields = ["author_name", ("date_of_birth", "date_of_death")]
    inlines = [BooksInline]


class ReservationInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""

    model = models.Reservation


class BookAdmin(admin.ModelAdmin):
    list_display = ("book_name", "author", "display_genre")
    inlines = [ReservationInline]


admin.site.register(models.Book, BookAdmin)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ["hash", "user__username", "book__book_name"]
    list_display = ("book", "hash", "status", "user", "date_of_issue", "date_of_return")
    list_filter = ("status", "date_of_issue", "date_of_return")
    readonly_fields = ("hash", "book", "user", "date_of_issue")
    fields = ("hash", "book", "status", "date_of_issue", "date_of_return", "user")

    def save_model(self, request, obj, form, change):
        field_status = "status"
        if (
            change
            and field_status in form.changed_data
            and form.cleaned_data.get(field_status) == models.Reservation.Status.ISSUED
        ):
            obj.date_of_return = datetime.now().date() + timedelta(days=30)
        if (
            change
            and field_status in form.changed_data
            and form.cleaned_data.get(field_status) == models.Reservation.Status.CLOSED
        ):
            book = models.Book.objects.filter(id=obj.book.id).first()
            book.books_in_stock += 1
            book.save()
        super().save_model(request, obj, form, change)
