from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers

from education.models import Lesson, LessonView
from product.models import Access

""" The Second part of Tasks """

""" TASK 1 """
""" Реализовать API для выведения списка всех уроков
    по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра. """


class LessonSerializer(serializers.ModelSerializer):
    """ The serializator for LessonViewSet """

    viewed = serializers.SerializerMethodField()
    view_time_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_viewed(self, obj):
        user = self.context['request'].user
        lesson_views = obj.lessonview_set.filter(user=user)
        if lesson_views:
            total_view_time = sum(view.view_time_seconds for view in lesson_views)
            return total_view_time >= obj.duration * 0.8
        return False

    def get_view_time_seconds(self, obj):
        user = self.context['request'].user
        lesson_views = obj.lessonview_set.filter(user=user)
        if lesson_views:
            total_view_time = sum(view.view_time_seconds for view in lesson_views)
            return total_view_time
        return 0


""" TASK 2 """
""" Реализовать API с выведением списка уроков
    по конкретному продукту к которому пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра,
    а также датой последнего просмотра ролика. """


class LessonWithStatusSerializer(serializers.ModelSerializer):
    """ The serializator for LessonWithStatusViewSet """

    viewed = serializers.SerializerMethodField()
    view_time_seconds = serializers.SerializerMethodField()
    last_view_date = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'url', 'duration', 'viewed', 'view_time_seconds', 'last_view_date']

    def get_viewed(self, obj):
        user = self.context['request'].user
        lesson_views = obj.lessonview_set.filter(user=user)
        if lesson_views:
            total_view_time = sum(view.view_time_seconds for view in lesson_views)
            return total_view_time >= obj.duration * 0.8
        return False

    def get_view_time_seconds(self, obj):
        user = self.context['request'].user
        lesson_views = obj.lessonview_set.filter(user=user)
        if lesson_views:
            total_view_time = sum(view.view_time_seconds for view in lesson_views)
            return total_view_time
        return 0

    def get_last_view_date(self, obj):
        user = self.context['request'].user
        lesson_views = obj.lessonview_set.filter(user=user).order_by('-view_date')
        if lesson_views:
            return lesson_views[0].view_date
        return None


""" TASK 3 """
""" Реализовать API для отображения статистики по продуктам.
    Необходимо отобразить список всех продуктов на платформе,
    к каждому продукту приложить информацию:
        Количество просмотренных уроков от всех учеников.
        Сколько в сумме все ученики потратили времени на просмотр роликов.
        Количество учеников занимающихся на продукте.
        Процент приобретения продукта 
        (рассчитывается исходя из количества полученных доступов
        к продукту деленное на общее количество пользователей
        на платформе). """


class ProductStatisticsSerializer(serializers.ModelSerializer):
    """ The serializator for ProductStatisticsViewSet """

    product_name = serializers.CharField(source='product.product_name')
    lessons_viewed = serializers.SerializerMethodField()
    total_view_time_seconds = serializers.SerializerMethodField()
    num_students = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Access
        fields = ['product_name', 'lessons_viewed', 'total_view_time_seconds', 'num_students', 'purchase_percentage']

    def get_lessons_viewed(self, obj):
        return LessonView.objects.filter(lesson__products=obj.product, viewed=True).count()

    def get_total_view_time_seconds(self, obj):
        return LessonView.objects.filter(lesson__products=obj.product).aggregate(total_time=Sum('view_time_seconds'))[
            'total_time'] or 0

    def get_num_students(self, obj):
        return Access.objects.filter(product=obj.product).count()

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        product_users = Access.objects.filter(product=obj.product).count()
        if total_users == 0:
            return 0
        return (product_users / total_users) * 100
