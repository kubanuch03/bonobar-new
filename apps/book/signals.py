from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver


from apps.book.models import Book
from apps.table.models import Table


@receiver(post_save, sender=Book)
def update_table_occupated_status_on_save(sender, instance, created, **kwargs):
    if created:
        for table in instance.tables.all():
            table.occupated = True
            table.save()


@receiver(pre_delete, sender=Book)
def update_table_occupated_status_on_delete(sender, instance, **kwargs):
    tables = instance.tables.all()

    for table in tables:
        if not table.books.exclude(id=instance.id).exists():
            table.occupated = False
            table.save()


@receiver(m2m_changed, sender=Book.tables.through)
def update_table_occupated_status_on_m2m_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        if reverse:
            for table_id in pk_set:
                table = Table.objects.get(pk=table_id)
                table.occupated = True
                table.save()
        else:
            for book_id in pk_set:
                book = Book.objects.get(pk=book_id)
                for table in book.tables.all():
                    table.occupated = True
                    table.save()
    elif action in ["post_remove", "post_clear"]:
        if reverse:
            for table_id in pk_set:
                table = Table.objects.get(pk=table_id)
                if not table.books.exists():
                    table.occupated = False
                    table.save()
        else:
            for book_id in pk_set:
                book = Book.objects.get(pk=book_id)
                for table in book.tables.all():
                    if not table.books.exists():
                        table.occupated = False
                        table.save()
