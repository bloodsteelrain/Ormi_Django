from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path(패턴, 매핑) /blog/
    # path('', views.index), # FBV
    # 글 목록 조회
    path('', views.List.as_view(), name='list'), # /blog/
    # 글 상세 조회
    path('detail/<int:pk>/', views.Detail.as_view(), name='detail'), # /blog/detail/1
    # 글 작성
    path('write/', views.Write.as_view(), name='write'), # /blog/write/
    # 글 수정
    path('detail/<int:pk>/edit/', views.Update.as_view(), name='edit'),
    # 글 삭제
    path('detail/<int:pk>/delete/', views.Delete.as_view(), name='delete'),
    # 댓글 작성
    # 댓글 삭제
]