
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# urlpatterns — список маршрутов проекта
# Django проверяет их по порядку
urlpatterns = [

    # Админ-панель Django
    # URL: /admin/
    path('admin/', admin.site.urls),

    # Все URL, начинающиеся с /cart/,
    # будут переданы в cart/urls.py
    # namespace='cart' нужен для уникальных имён URL
    path('cart/', include('cart.urls', namespace='cart')), 

    # Главная часть сайта
    # Пустая строка '' означает корень сайта (/)
    # Все остальные маршруты ищутся в main/urls.py
    path('', include('main.urls', namespace='main')), 

]

# В режиме DEBUG Django сам раздаёт медиа-файлы
# (из MEDIA_ROOT по адресу MEDIA_URL)
# В продакшене так НЕ делают
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)