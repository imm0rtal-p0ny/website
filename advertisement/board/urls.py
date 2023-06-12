from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('board/<int:pk>', views.BoardDetailView.as_view(), name='board'),
    path('create_board', views.BoardCreateView.as_view(), name='create_board'),
    path('update_board/<int:pk>', views.BoardUpdateView.as_view(), name='update_board'),
    path('<str:name>', views.DivisionBoardListView.as_view(), name='division'),
    path('user_boards/<int:pk>', views.UserBoardListView.as_view(), name='user_boards'),
    path('delete_board/<int:pk>', views.delete_board, name='delete_board'),
    path('add_photo/<int:pk>', views.delete_board, name='add_photo'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


