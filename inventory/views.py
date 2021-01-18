from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.core import serializers
from weasyprint import HTML
from django.core.serializers.json import DjangoJSONEncoder
from .serializers import InventorySerializer
from .models import Order, Item, Medication, Formation, Categorical_dose, Type, Kind_name
from django.http.response import JsonResponse
from xhtml2pdf import pisa
from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
from bidi import algorithm as bidialg
from django.http import HttpResponse
from django.template.loader import get_template
from .make_pdf import *
import datetime


def index(request):
    return render(request, 'inventory/datatablesTest.html')


def excel(request):  # https://stackoverflow.com/questions/27180190/django-using-objects-values-and-get-foreignkey-data-in-template
    if request.method == 'GET':
        medic = Medication.objects.all()
        serializer = InventorySerializer(medic, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)


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


def to_html(request):
    main_dict = make_cat_dict()
    file_name_list = []
    for key in main_dict.keys():
        print(main_dict[key])
        # file_name = str(datetime.datetime.today().date()) + '_' + str(key)
        # file_name_list.append(file_name)
        # makeToc(file_name=file_name, cat_dict=main_dict[key])


def to_pdf(request, context_dict={}):
    template_src = "inventory/test.html"
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # from bidi import algorithm as bidialg
    # from xhtml2pdf import pisa
    #
    # HTMLINPUT = """
    #             <!DOCTYPE html>
    #             <html>
    #             <head>
    #                <meta http-equiv="content-type" content="text/html; charset=utf-8">
    #                <style>
    #                   @page {
    #                       size: a4;
    #                       margin: 1cm;
    #                   }
    #
    #                   @font-face {
    #                       font-family: DejaVu;
    #                       src: url(my_fonts_dir/DejaVuSans.ttf);
    #                   }
    #
    #                   html {
    #                       font-family: DejaVu;
    #                       font-size: 11pt;
    #                   }
    #                </style>
    #             </head>
    #             <body>
    #                <div>Something in English - משהו בעברית</div>
    #             </body>
    #             </html>
    #             """
    #
    # pdf = pisa.CreatePDF(bidialg.get_display(HTMLINPUT, base_dir="L"), outpufile)

    # This part will create the pdf.
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class OrdersView(generic.ListView):
    template_name = 'inventory/orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.order_by('-created')


class OrderView(generic.DetailView):
    model = Order
    template_name = 'inventory/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['lineitems'] = context['order'].orderitem_set.order_by("item__vendor")
        return context


class ItemView(generic.DetailView):
    model = Item
    template_name = 'inventory/item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context['lineitems'] = context['item'].orderitem_set.order_by("order__order_date")
        return context


def html_to_pdf_view(request):
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
    # print("in invent: ", formations_in_inventory)

    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string('test_template.html', {'form_dict': form_dict})

    html = HTML(string=html_string)  # , base_url=request.build_absolute_uri()
    html.write_pdf(target='/tmp/mypdf.pdf')
    # html.write_png(target='/tmp/mypng.png')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    # with fs.open('mypng.png') as pdf:
    #     response = HttpResponse(pdf, content_type='application/png')
    #     response['Content-Disposition'] = 'attachment; filename="mypng.png"'
    #     return response

    # return HttpResponse(html_string)


# https://dev.to/djangotricks/how-to-create-pdf-documents-with-django-in-2019-5gb9
def generate_pdf(request):  # https://stackoverflow.com/questions/43539702/attach-img-file-in-pdf-weasyprint
    # html_template = get_template('test_template.html')
    # user = request.user
    # rendered_html = html_template.render().encode(encoding="UTF-8")
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
    # print("in invent: ", formations_in_inventory)

    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string('test_template.html', {'form_dict': form_dict})

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target='/tmp/mypdf.pdf')  # stylesheets=[CSS(settings.STATIC_ROOT +  '/css/generate_html.css')]
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="generate_html.pdf"'

    return http_response
