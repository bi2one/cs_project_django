from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^CS_SCM/', include('CS_SCM.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'csscm.consumers.views.index'),
    (r'^/$', 'csscm.consumers.views.index'),
    (r'^logout/$', 'csscm.consumers.views.logout_user'),
    (r'^join/$', 'csscm.consumers.views.join_user'),
    (r'^refund_buyingitem/(?P<item_id>\d+)/$', 'csscm.consumers.views.refund_buyingitem'),
    (r'^itemview/(?P<item_id>\d+)/$', 'csscm.consumers.views.itemview'),
    (r'^order/$', 'csscm.consumers.views.order'),
    (r'^manage/$', 'csscm.consumers.views.manage'),
    (r'^finish_order/(?P<buying_item_id>\d+)/$', 'csscm.consumers.views.finish_order'),
    (r'^refund_order/(?P<buying_item_id>\d+)/$', 'csscm.consumers.views.refund_order'),
    (r'^update_selling_item/(?P<selling_item_id>\d+)/$', 'csscm.consumers.views.update_selling_item'),
    (r'^update_selling_item/$', 'csscm.consumers.views.update_selling_item'),
    (r'^update_item/(?P<item_id>\d+)/$', 'csscm.consumers.views.update_item'),
    (r'^update_stock_item/(?P<item_id>\d+)/$', 'csscm.consumers.views.update_stock_item'),
    (r'^update_stock_item/$', 'csscm.consumers.views.update_stock_item'),
    (r'^request_factory_item/(?P<item_id>\d+)/$', 'csscm.consumers.views.request_factory_item'),
)
