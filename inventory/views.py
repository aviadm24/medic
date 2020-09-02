from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

from weasyprint import HTML

from .models import Order, Item, Medication, Formation, Categorical_dose, Type, Kind_name


def index(request):
    return render(request, 'inventory/index.html')


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
