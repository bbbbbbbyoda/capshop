from django.urls import path, include
from . import views


urlpatterns = [
    path('product-list/', views.ProductListView.as_view()),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view()),
    path('home-page/', views.HomePageView.as_view()),
    path('order/', views.OrderListCreateView.as_view())
]
