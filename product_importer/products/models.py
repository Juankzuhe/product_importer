from django.db.models import BooleanField, CharField, DateTimeField, Model


class Product(Model):
    """Product Model"""

    sku = CharField(max_length=500, unique=True)
    name = CharField(max_length=500)
    description = CharField(max_length=500)
    is_active = BooleanField("active", default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
