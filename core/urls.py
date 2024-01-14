from django.urls import path

from . import views

urlpatterns = [
    path("",views.store, name='store'),
    path("<int:pk>/",views.detail, name="detail"),
    path("checkout/", views.checkout, name='checkout'),
    path("cart/",views.cart, name='cart'),
    path("signin/",views.signin, name="signin"),
    path("signup/",views.signup, name="signup"),
    path("logout/", views.logoutPage, name="logout"),
    path('update_item/',views.update_item, name='update_item'),
    path('process_order/',views.processOrder, name='processOrder')
]