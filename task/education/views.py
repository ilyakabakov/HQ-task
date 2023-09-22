from rest_framework import viewsets, permissions

from education.models import Lesson
from education.serializers import LessonSerializer, LessonWithStatusSerializer, ProductStatisticsSerializer
from product.models import Access

""" TASK 1 """


class LessonViewSet(viewsets.ModelViewSet):
    """ Viewset for list of all lessons for all products where user have access """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = Access.objects.filter(user=user).values_list('product_id', flat=True)
        return Lesson.objects.filter(products__in=accessible_products)


""" TASK 2 """


class LessonWithStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for list of lessons with status, view time, and last view date for a specific product. """

    serializer_class = LessonWithStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        accessible_products = Access.objects.filter(user=user, product_id=product_id)
        if accessible_products.exists():
            return Lesson.objects.filter(products=product_id)
        else:
            return Lesson.objects.none()


""" TASK 3 """


class ProductStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for product statistics. """

    serializer_class = ProductStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = Access.objects.filter(user=user)
        return accessible_products
