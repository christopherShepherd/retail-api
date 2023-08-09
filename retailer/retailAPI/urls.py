from django.urls import path
from . import views


urlpatterns = [
    path('groups/<groupName>/users/',
          views.ManageGroupsView.as_view({'get':'list', 'post':'create',}),
          name="managegroups"),  # groups['manager', 'delivery-crew']
    path('groups/<groupName>/users/<int:pk>/',
          views.ManageGroupsView.as_view({'delete':'destroy',}),
          name="removefromgroup"),
    path('items/',
         views.ItemsViewSet.as_view({'get':'list',
                                     'post':'create'}), name="items"),
    path('items/<title>/',
         views.ItemsViewSet.as_view({'get':'retrieve', 'put':'update',
                                     'patch':'partial_update',
                                     'delete':'destroy',}), name="singleitem"),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('cart/items/', views.CartView.as_view(), name="cart"),
    path('orders/', views.OrderViewSet.as_view({'get':'list',
                                                'post':'create',}),
                                                name='orders'), 
    path('orders/<int:pk>/',
          views.OrderViewSet.as_view({'get':'retrieve',
                                      'put':'update',
                                      'patch':'partial_update',
                                      'delete':'destroy'}), name='singleorder'),
]
