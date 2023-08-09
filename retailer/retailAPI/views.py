from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
import decimal
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import (UserSerializer, ItemSerializer, CategorySerializer,
                          CartSerializer, OrderSerializer)
from .models import Item, Cart, Order, OrderItem, Category
from .pagination import CustomPageNumberPagination
from .permissions import IsManager, IsDeliveryCrew


class ManageGroupsView(viewsets.ViewSet):
    """
    list: show all users belonging to passed group
    create: add passed username to specified group
    destroy: remove user of primary-key from specified group
    """

    permission_classes = [IsAdminUser|IsManager]
    throttle_classes = [UserRateThrottle]

    def list(self, request, groupName):
        requested_group = get_object_or_404(Group, name=groupName)
        grouplist = User.objects.all().filter(groups__name=groupName)
        serialized_list = UserSerializer(grouplist, many=True)
        return Response(serialized_list.data, status.HTTP_200_OK)

    def create(self, request, groupName):
        username = request.data['username']
        if username:
            requested_group = get_object_or_404(Group, name=groupName)
            requested_user = get_object_or_404(User, username=username)
            requested_group.user_set.add(requested_user)
            return Response({"message": "assigned to group"}, status.HTTP_201_CREATED)
        else:
            return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, groupName, pk):
        requested_group = get_object_or_404(Group, name=groupName)
        requested_user = get_object_or_404(User, pk=pk)
        requested_group.user_set.remove(requested_user)
        return Response({"message": "removed from group"}, status.HTTP_200_OK)


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'title'
    ordering_fields = ['price']
    filterset_fields = ['category__title']
    pagination_class = CustomPageNumberPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAdminUser|IsManager]
        
        return [permission() for permission in permission_classes]

    def list(self, request):
        # disable pagination if 'page' not specified in endpoint
        pagination = request.query_params.get('page')
        if not pagination:
            self.pagination_class = None
        return super(ItemsViewSet, self).list(self, request)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset= Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        quantity = serializer.validated_data['quantity']
        unitprice = item.price
        totalprice = unitprice * quantity

        serializer.save(user=self.request.user, price=totalprice, unit_price=unitprice)

    def destroy(self, request):
        cart_items = self.get_queryset()
        if cart_items:
            for item in cart_items:
                item.delete()

        return Response({"message": "cart empty"}, status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering_fields = ['total', 'date']
    filterset_fields = ['status']
    pagination_class = CustomPageNumberPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'partial_update':
            permission_classes = [IsAdminUser|IsManager|IsDeliveryCrew]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAdminUser|IsManager]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='delivery-crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        return Order.objects.all().filter(user=self.request.user)
       
    def create(self, request):
        user = self.request.user
        cartitems = Cart.objects.all().filter(user=user)

        if cartitems:
            totalprice = decimal.Decimal('0.0')
            for item in cartitems:
                totalprice += item.price

            neworder = Order.objects.create(user=user, total=totalprice)

            for cartitem in cartitems:
                OrderItem.objects.create(order=neworder,
                                         item=cartitem.item,
                                         quantity=cartitem.quantity,
                                         unit_price=cartitem.unit_price,
                                         price=cartitem.price)
                cartitem.delete()

            return Response({"message":"Order Placed",
                             "Your Order Number":neworder.id}, status=status.HTTP_201_CREATED)

        return Response({"message":"Please add items to the cart before placing order"},
                         status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        pagination = request.query_params.get('page')
        if not pagination:
            self.pagination_class = None
        return super(OrderViewSet, self).list(self, request)

