
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contacts/',views.contacts,name='contacts'),
    path('login/',views.login_users,name='login'),
    path('product/<str:name>/',views.product,name='product'),
    path('products/',views.products,name='products'),
    path('products/<str:cuis>',views.products_cuis,name='products_cuis'),
    path('shoppingcart/',views.shoppingcart,name='shoppingcart'),
    path('logout/', views.logout_users, name="logout"),
    path('signup/',views.signup,name='signup'),

    path('add/',views.add_product,name='add'),
    path('update/<str:name>',views.update_product,name='update'),
    path('delete/<str:name>',views.delete_product,name='delete'),

    path('update_item/',views.update_item,name='update_item'),

    
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  