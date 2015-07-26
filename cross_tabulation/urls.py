from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'cross_tabluation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^upload/', 'c_tabulation.views.upload_or_render_csv', name="upload_csv"),
    url(r'^showtabulationdata/', 'c_tabulation.views.show_tabulation', name="showtabulationdata"),
    url(r'^savetabulateddata/', 'c_tabulation.views.save_tab_data', name="savetabulateddata"),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
