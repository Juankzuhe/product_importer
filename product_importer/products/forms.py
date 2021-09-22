from django.forms.forms import FileField, Form


class CsvImportProductForm(Form):
    csv_file = FileField()
