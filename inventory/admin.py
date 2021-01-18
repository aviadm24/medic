# import csv
from django.db.models import Count, Q
import datetime
import unicodecsv as csv
from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import get_object_or_404, render, redirect
from import_export.admin import ImportExportModelAdmin
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.core import serializers
from weasyprint import HTML
from django.contrib.auth.models import Group, User
import pandas as pd
from inventory.models import Item, Category, Unit, Vendor, PTAO, Order, OrderItem,\
    Formation, Categorical_dose, Dose, Type, Company, Manufacturer, Manufacturing_country, Kind_name, Medication
from .make_pdf import *
from xhtml2pdf import pisa
from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template

admin.site.unregister(Group)
admin.site.unregister(User)


def make_cat_dict():
    formations_queryset = Formation.objects.all()
    categorical_doses = Categorical_dose.objects.all()
    types = Type.objects.all()
    # kind_names = Kind_name.objects.all()
    form_dict = {}
    for form in formations_queryset:
        print(form.name)
        # formations_in_inventory = Medication.objects.filter(formation__in=formations_queryset)
        formation_query = Medication.objects.filter(formation=form)
        cat_dict = {}
        for category in categorical_doses:
            elem_list = []
            print(category.name)
            category_query = formation_query.filter(categorical_dose=category)
            print(category_query)
            type_list = []
            for m_type in types:
                type_query = category_query.filter(m_type=m_type)
                print(type_query)
                for elem in type_query:
                    print("price: ", elem.price)
                    # elem_list.append(str(m_type))
                    # elem_list.append(str(kind))
                    # elem_list.append(str(elem.price))
                    type_list.append("{} - {} - {}".format(m_type.name, elem.kind_name, elem.price))
            cat_dict[category.name] = type_list
        form_dict[form] = cat_dict
    return form_dict


def sum_dict():
    # categorical_doses = Categorical_dose.objects.all()
    # kind_count = Count('Medication', filter=Q(formation__m_type__categorical_dose__in=categorical_doses))
    #
    formations_queryset = Formation.objects.all()
    categorical_doses = Categorical_dose.objects.all()
    types = Type.objects.all()
    form_dict = {}
    type_dict = {}
    for form in formations_queryset:
        print(form.name)
        # formations_in_inventory = Medication.objects.filter(formation__in=formations_queryset)
        formation_query = Medication.objects.filter(formation=form)
        cat_dict = {}
        for category in categorical_doses:
            print("\t"+category.name)
            category_query = formation_query.filter(categorical_dose=category)
            # print(category_query)
            elem_sum = 0
            for m_type in types:
                print("\t\t"+m_type.name)
                type_query = category_query.filter(m_type=m_type)
                # print(type_query)

                for elem in type_query:
                    print("amount: ", elem.amount)
                    elem_sum += elem.amount
            type_dict["{}_{}_{}".format(form.name, category.name, m_type.name)] = elem_sum
        # cat_dict[category.name] = elem_sum
    # form_dict[form.name] = cat_dict
    return type_dict


class ExportHTMLMixin:
    def export_html(self, request, queryset):
        form_dict = make_cat_dict()
        return render(request, 'pdf_template.html', {'form_dict': form_dict})
        # html_string = render_to_string('test_template.html', {'form_dict': form_dict})
        #
        # html = HTML(string=html_string)  # , base_url=request.build_absolute_uri()
        # html.write_pdf(target='/tmp/mypdf.pdf')

    export_html.short_description = 'דו"ח html'


class ExportPdfMixin:
    def export_pdf(self, request, queryset):
        # form_dict = make_cat_dict()
        # html_string = render_to_string('test_template.html', {'form_dict': form_dict})
        #
        # html = HTML(string=html_string)  # , base_url=request.build_absolute_uri()
        # html.write_pdf(target='/tmp/mypdf.pdf')
        # # html.write_png(target='/tmp/mypng.png')
        #
        # fs = FileSystemStorage('/tmp')
        # with fs.open('mypdf.pdf') as pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        #     return response

        # HTML('https://www.hamerkaha.co.il/menu-cannabis/?fbclid=IwAR1cyNigDS45zoBuOgZv89Vs4DLqcBbmHz0UgGi6ndF25h2tNlLPYi0no1U').write_pdf(target='/tmp/mypdf.pdf')
        # fs = FileSystemStorage('/tmp')
        # with fs.open('mypdf.pdf') as pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        #     return response
        main_dict = make_cat_dict()
        file_name_list = []
        for key in main_dict.keys():
            file_name = str(datetime.datetime.today().date())+'_'+str(key)
            file_name_list.append(file_name)
            makeToc(file_name=file_name, cat_dict=main_dict[key])
        # fs = FileSystemStorage('/temp')
        # with fs.open(file_name_list[0]) as pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name_list[0])
        #     return response

        # https://stackoverflow.com/questions/42814732/how-to-return-multiple-files-in-httpresponse-django
        # def zipFiles(files):
        #     outfile = StringIO()  # io.BytesIO() for python 3
        #     with zipfile.ZipFile(outfile, 'w') as zf:
        #         for n, f in enumerate(files):
        #             zf.writestr("{}.csv".format(n), f.getvalue())
        #     return outfile.getvalue()
        #
        # zipped_file = zip_files(myfiles)
        # response = HttpResponse(zipped_file, content_type='application/octet-stream')
        # response['Content-Disposition'] = 'attachment; filename=my_file.zip'

    export_pdf.short_description = 'דו"ח מעוצב'


# def to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#
#     # This part will create the pdf.
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


class ExportPdfMixin2:
    def render_to_pdf(self, request, queryset):
        return render(request, 'inventory/test.html')
        # to_pdf("'inventory/test.html'")
    render_to_pdf.short_description = 'דו"ח מעוצב2'


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # google this - pandas index not showing up in csv file when using to_csv
        # form_dict = make_cat_dict()
        # df = pd.DataFrame(data=form_dict)
        # print(df)
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=test.csv'
        # df.to_csv(response, index=False)
        # return response

        # meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        #
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=doch.csv'  # 'attachment; filename={}.xlsx'.format(meta)
        # writer = csv.writer(response, encoding="utf8")   # https://answers.microsoft.com/en-us/msoffice/forum/all/how-to-open-csv-file-of-hebrew-language/8963c913-fb3d-4f22-866e-d373366ba196
        # writer.writerow(field_names)
        # for obj in queryset:
        #     row = writer.writerow([getattr(obj, field) for field in field_names])
        # return response

        # cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
        #         'Price': [32000, 35000, 37000, 45000]
        #         }
        #
        # df = pd.DataFrame(cars, columns=['Brand', 'Price'])
        # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename="filename.xlsx"'
        # df.to_excel(response)
        # return response

        # return render(request, 'inventory/datatablesTest.html')
        return render(request, 'inventory/excel.html')



    export_as_csv.short_description = 'דו"ח מלא'


def excel(request):
    object_list = Medication.objects.all()  # or any kind of queryset
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')


class MedicBookPageMixin:
    def export_page_num(self, request, queryset):
        meta = self.model._meta
        field_names = ['pharma_code', 'page_num']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_page_num.short_description = 'דו"ח ספר הסמים'


class MedicSumMixin:
    def export_sum(self, request, queryset):
        type_dict = sum_dict()
        print("dict: ", type_dict)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=sum_doch.csv'
        writer = csv.writer(response)
        for key in type_dict.keys():
            row = writer.writerow([key, type_dict[key]])

        return response

    export_sum.short_description = 'דו"ח כמות'


class MedicineAdmin(admin.ModelAdmin, ExportCsvMixin, ExportPdfMixin, ExportPdfMixin2, MedicBookPageMixin, MedicSumMixin, ExportHTMLMixin):
    date_hierarchy = 'date_added'

    list_filter = ('kind_name', 'manufacturer', 'date_added', 'formation')
    search_fields = ('name', 'manufacturer', 'formation')
    actions = ["export_as_csv", "export_pdf", "render_to_pdf", "export_page_num", "export_sum", "export_html"]


admin.site.register(Medication, MedicineAdmin)


for model in (Formation, Categorical_dose, Type, Company, Manufacturer, Manufacturing_country):
    admin.site.register(model)
