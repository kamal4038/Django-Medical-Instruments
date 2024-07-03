


from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='home'),
    path('nursing_services/',views.nursing_services,name='nursing_services'),
    path('health/',views.health,name='health'),
    path('equipments/',views.equipments,name='equipments'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login'),
    # path('sign_in/',views.login_view,name='sign_in'),
    path('collections/',views.collections,name='collections'),
      
    path('index/',views.index,name='index'),  
    
    path('logout/',views.logout_page,name='logout'),
    path('navbar/',views.navbar,name='navbar'),
     path('products/',views.products,name='products'),

   #============ CART,RENT,BUY URLS ===========================
    
   path('adc/<int:productid>/',views.add_to_cart,name='adc'),
  
   path('adr/',views.add_to_rent,name='adr'),
  
   path('adb/',views.add_to_buy,name='adb'),

   #============ DISPLAY OF CART,RENT,BUY URLS =================
   path('cart/',views.Cart_display,name='cart'),
   path('rented/',views.Rented_display,name='rented'),
   path('ordered/',views.Ordered_display,name='ordered'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
