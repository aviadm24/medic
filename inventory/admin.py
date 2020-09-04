import csv
from django.http import HttpResponse
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.auth.models import Group, User
import pandas as pd
from inventory.models import Item, Category, Unit, Vendor, PTAO, Order, OrderItem,\
    Formation, Categorical_dose, Dose, Type, Company, Manufacturer, Manufacturing_country, Kind_name, Medication

admin.site.unregister(Group)
admin.site.unregister(User)


def make_cat_dict():
    formations_queryset = Formation.objects.all()
    categorical_doses = Categorical_dose.objects.all()
    types = Type.objects.all()
    kind_names = Kind_name.objects.all()
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
            for m_type in types:
                type_query = category_query.filter(m_type=m_type)
                print(type_query)
                for kind in kind_names:
                    kind_query = type_query.filter(kind_name=kind)
                    for elem in kind_query:
                        print("price: ", elem.price)
                        elem_list.append(str(m_type))
                        elem_list.append(str(kind))
                        elem_list.append(str(elem.price))
            cat_dict[category] = elem_list
        form_dict[form] = cat_dict
    return form_dict


class ExportPdfMixin:
    def export_as_pdf(self, request, queryset):
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

        HTML('https://www.hamerkaha.co.il/menu-cannabis/?fbclid=IwAR1cyNigDS45zoBuOgZv89Vs4DLqcBbmHz0UgGi6ndF25h2tNlLPYi0no1U').write_pdf(target='/tmp/mypdf.pdf')
        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
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

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class MedicBookPageMixin:
    def export_page_num(self, request, queryset):
        # google this - pandas index not showing up in csv file when using to_csv
        # form_dict = make_cat_dict()
        # df = pd.DataFrame(data=form_dict)
        # print(df)
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=test.csv'
        # df.to_csv(response, index=False)
        # return response

        meta = self.model._meta
        field_names = ['pharma_code', 'page_num']

        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_page_num.short_description = "Export Page_numbers"


# class OrderItemInline(admin.StackedInline):
#     model = OrderItem
#     extra = 1
#
#
# class ItemAdmin(admin.ModelAdmin):
#     date_hierarchy = 'date_added'
#
#     fieldsets = [
#         (None, {'fields': ['name', 'chem_formula', 'category']}),
#         ('Vendor Information', {'fields': ['vendor', 'catalog', 'manufacturer',
#                                            'manufacturer_number',
#                                            'size', 'unit',]}),
#         (None, {'fields': ['parent_item', 'comments']})
#     ]
#
#     list_display = ('name', 'category', 'date_added',)
#     list_filter = ('category', 'vendor', 'manufacturer', 'date_added')
#     search_fields = ('name', 'chem_formula', 'manufacturer_number', 'comments')
#     inlines = (OrderItemInline,)
#     # actions = ["export_as_csv"]


# admin.site.register(Item, ItemAdmin)


class MedicineAdmin(admin.ModelAdmin, ExportCsvMixin, ExportPdfMixin, MedicBookPageMixin):
    date_hierarchy = 'date_added'

    list_filter = ('name', 'manufacturer', 'date_added')
    search_fields = ('name', 'manufacturer', 'comments')
    actions = ["export_as_csv", "export_as_pdf", "export_page_num"]


admin.site.register(Medication, MedicineAdmin)

# class OrderAdmin(admin.ModelAdmin):
#     date_hierarchy = 'order_date'
#     fields = ('name', 'order_date', 'ordered_by', 'ordered', 'ptao',)
#     list_display = ('name', 'item_count', 'order_date', 'ordered', 'ptao')
#     list_filter = ('ordered', 'ptao', 'ordered_by')
#     search_fields = ('name',)
#     inlines = (OrderItemInline,)
#
# admin.site.register(Order, OrderAdmin)
#
# class OrderItemAdmin(admin.ModelAdmin):
#     date_hierarchy = 'date_arrived'
#     fields = ('units_purchased', 'cost', 'date_arrived', 'serial', 'uva_equip',
#               'location', 'expiry_years', 'reconciled')
#     list_display = ('name', 'order_date', 'date_arrived', 'total_price', 'location')
#     list_filter = ('item__name', 'order__order_date', 'date_arrived', 'location')
#
# admin.site.register(OrderItem, OrderItemAdmin)
#
# class PTAOAdmin(admin.ModelAdmin):
#     fields = ('code', 'description', 'expires')
#     list_display = fields + ('active',)
#
#
# admin.site.register(PTAO, PTAOAdmin)
#
# for model in (Category, Unit, Manufacturer, Vendor):
#     admin.site.register(model)


for model in (Formation, Categorical_dose, Dose, Type, Company, Manufacturer, Manufacturing_country, Kind_name):
    admin.site.register(model)
