from django.forms.forms import Form, FileField


class CsvImportProductForm(Form):
    csv_file = FileField()
