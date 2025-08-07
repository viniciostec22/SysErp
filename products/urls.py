from django.urls import path
from . import views

app_name = 'products' # Define um namespace para as URLs da app

urlpatterns = [
    # URLs para Marcas
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<uuid:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('brands/<uuid:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),

    # URLs para Categorias
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<uuid:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<uuid:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # URLs para Produtos
    path('', views.ProductListView.as_view(), name='product_list'), # URL para listar produtos
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<uuid:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<uuid:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]
