from django.contrib.auth.models import User
from django.urls import path, reverse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This view set automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]


class ProductViewSet(viewsets.ModelViewSet):
    """
    This view set automatically provides `list` and `retrieve` actions.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save({})


@api_view()
def root(request):
    return Response({
        'user-list', reverse('user-list'),
        'user-detail', reverse('user-detail', kwargs={'pk': 1}),
        'product-list', reverse('product-list'),
        'product-detail', reverse('product-detail', kwargs={'pk': 1}),
        'user-profile', reverse('user-profile'),
        'change-active-status', reverse('change-active-status', kwargs={'pk': 1}),
    })


@api_view()
def user_profile(request):
    if request.user.is_authenticated:
        return Response({
            'username': request.user.first_name,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'date_joined': request.user.date_joined,
            'last_login': request.user.last_login,
        })
    return Response({
        'error': 'You need to Login'
    })


class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


@api_view(["POST"])
@authentication_classes([SessionCsrfExemptAuthentication])
@permission_classes([IsAuthenticated])
def change_active_status(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.filter(user=request.user, pk=pk).first()
        if product:
            if product.is_not_deactivatable():
                return Response({
                    'error': "You cannot deactivate a product within first 2 months"
                })
            else:
                if product.is_active:
                    product.is_active = False
                else:
                    product.is_active = True
                product.save()
                return Response({
                    'is_active': product.is_active,
                })
        else:
            return Response({'error': 'Product not found!'})
    return Response({'error': 'You need to login!'})


