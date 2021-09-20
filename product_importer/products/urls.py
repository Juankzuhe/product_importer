from django.urls import path

from product_importer.products.views import (
    product_index_view,
    product_create_view,
    product_update_view,
    product_delete_all_view
)

app_name = "products"
urlpatterns = [
    path("", view=product_index_view, name="index"),
    path("add/", view=product_create_view, name="add"),
    path("delete/", view=product_delete_all_view, name="delete"),
    path("update/<int:pk>", view=product_update_view, name="update"),

]
