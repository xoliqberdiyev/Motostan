from django.urls import path

from product.api.v1 import views


urlpatterns = [
    path('discounted-products/', views.DiscountedProductApiView.as_view(), name='discounted-product'),
    path('top-products/', views.TopProductApiView.as_view(), name='top-product'),
    # path('categories/', views.ProductCategoryApiView.as_view(), name='product-categories'),
    path('brands/', views.ProductBrandApiView.as_view(), name='product-brands'),
    path('colors/', views.ProductColorApiView.as_view(), name='product-colors'),
    path('category/<int:category_id>/infos/', views.ProductInfoByCategoryApiView.as_view(), name='category-infos'),
    path('category/<int:category_id>/products/', views.ProductByCategoryApiView.as_view(), name='category-infos'),
    path('product/<int:id>/', views.ProductDetailApiView.as_view(), name='category-infos'),
    path('main-category/list/', views.MainCategoryApiView.as_view(), name='main-category'),
    path('categories/list/', views.CategoriesListApiView.as_view(), name='main-category'),
    path('search/', views.SearchApiView.as_view(), name='search'),
]

