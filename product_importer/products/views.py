import random

import pandas
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CsvImportProductForm
from .models import Product
from .tasks import import_products

form = CsvImportProductForm()


class ImportProductView(View):
    def get(self, request, *args, **kwargs):

        return render(request, "pages/home.html", context={"form": form})

    def post(self, request):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith(".csv"):
            messages.warning(request, "The wrong file type was uploaded")
            return HttpResponseRedirect(request.path_info)

        if request.is_ajax():
            try:
                dataframe = pandas.read_csv(csv_file)
                dataframe.drop_duplicates(subset=["sku"], keep="last")
                dataframe["is_active"] = random.choices([True, False], k=len(dataframe))
                dataset = dataframe.to_json(orient="records")
                print("step -- load")
                import_products.delay(dataset)
                print("step -- response")
                returnmsg = {"status_code": 200}
                print("imported successfully")
            except Exception as e:
                import traceback

                err = traceback.format_exc()
                print(str(err))
                print("Error While Importing Data: ", e)
                returnmsg = {"status_code": 500}

            return JsonResponse(returnmsg)


class ProductListView(ListView):
    template_name = "products/index.html"
    paginate_by = 10
    model = Product

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        object_list = self.model.objects.all()
        if query:
            object_list = object_list.filter(
                Q(name__icontains=query)
                | Q(sku__icontains=query)
                | Q(description__icontains=query)
            )

        if self.request.GET.get("is_active"):
            object_list = object_list.filter(
                is_active__exact=self.request.GET.get("is_active")
            )

        return object_list


product_index_view = ProductListView.as_view()


class ProductCreateView(CreateView):
    model = Product
    fields = (
        "name",
        "sku",
        "description",
        "is_active",
    )

    def get_success_url(self):
        return reverse("products:index")


product_create_view = ProductCreateView.as_view()


class ProductUpdateView(UpdateView):
    model = Product
    fields = (
        "name",
        "sku",
        "description",
        "is_active",
    )

    def get_success_url(self):
        return reverse("products:index")


product_update_view = ProductUpdateView.as_view()


class ProductDeleteAllView(View):
    def get(self, request, *args, **kwargs):
        Product.objects.all().delete()

        url = reverse("home")
        return HttpResponseRedirect(url)


product_delete_all_view = ProductDeleteAllView.as_view()
