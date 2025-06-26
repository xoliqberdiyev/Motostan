from django.urls import path

from product.api.v1 import views


urlpatterns = [
    path('discounted-products/', views.DiscountedProductApiView.as_view(), name='discounted-product'),
    path('first/category/<int:category_id>/products/', views.MainProductByCategoryApiView.as_view(), name='category-infos'),
    path('second/category/<int:category_id>/products/', views.SubProductByCategoryApiView.as_view(), name='category-infos'),
    path('fourth/category/<int:category_id>/products/', views.SubSubProductByCategoryApiView.as_view(), name='category-infos'),
    path('third/category/<int:category_id>/products/', views.ProductByCategoryApiView.as_view(), name='category-infos'),
    path('fifth/category/<int:category_id>/products/', views.ProductByFifthCategoryApiView.as_view(), name='category-infos'),
    path('product/<int:id>/', views.ProductDetailApiView.as_view(), name='category-infos'),
    path('categories/list/', views.CategoriesListApiView.as_view(), name='main-category'),
    path('search/', views.SearchApiView.as_view(), name='search'),
]

