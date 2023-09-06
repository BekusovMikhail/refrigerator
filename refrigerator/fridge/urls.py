from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/upload_video', views.VideoViewSet, basename="upload")

urlpatterns = [
    path("api/products/", views.GetProducts.as_view()),
    path("api/cameras/", views.GetCameras.as_view()),
    path("api/counters/", views.GetCounters.as_view()),
    path("api/users/", views.GetUsers.as_view()),
    path("api/products/<int:id>/", views.GetProducts.as_view()),
    path("api/cameras/<int:id>/", views.GetCameras.as_view()),
    path("api/counters/<int:id>/", views.GetCounters.as_view()),
    path("api/users/<int:id>/", views.GetUsers.as_view()),
    path("api/counters_by_camera/<int:id>/", views.GetCountersByCamera.as_view()),
    path("api/counters_by_product/<int:id>/", views.GetCountersByProduct.as_view()),
    path("api/cameras_by_user/<int:id>/", views.GetCamerasByUser.as_view()),
    path("api/cameras_by_username/<str:username>/", views.GetCamerasByUserUsername.as_view()),
    path("api/reg_user/", views.regUser),
    path("api/login_user/", views.loginUser),
    path("api/create_camera/", views.create_camera),
    path("api/delete_camera/", views.delete_camera),
    path("api/reset_all_counters/", views.reset_all_counters),
    path("api/launch_camera_process/", views.launch_camera_process),
    path("api/stop_camera_process/", views.stop_camera_process),
    path("api/add_counter/", views.add_counter),
    path("api/add_product/", views.add_product),
    path("api/delete_counter/<int:id>", views.DeleteCounter.as_view()),
    path("api/delete_product/<int:id>", views.DeleteProduct.as_view()),
    # path('api/video_2', views.VideoViewSet, name= 'video_list'),
    path('', include(router.urls)),
]
