from django.conf.urls import url
from django.urls import path

from inventory import views

app_name = "inventory"
urlpatterns = [
    url(r'^$', views.index, name='admin'),
    path('/redirect/', views.excel, name='excel_ajax_url'),
    path('/test/', views.test, name='test'),
    url(r'^pdf$', views.html_to_pdf_view, name='html_to_pdf_view'),
    # url(r'^pdf$', views.generate_pdf, name='html_to_pdf_view'),
    url(r'^orders/$', views.OrdersView.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', views.OrderView.as_view(), name='order'),
    url(r'^items/(?P<pk>\d+)/$', views.ItemView.as_view(), name='item')
]
# urlpatterns = patterns('myapp.views',
#                     url(regex=r'^$',
#                     view='myModel_asJson',
#                     name='my_ajax_url'),
# )