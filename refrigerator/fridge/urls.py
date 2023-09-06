from django.urls import include, path
from . import views

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
    path("api/reg_user/", views.regUser),
    path("api/log_user/", views.loginUser),
]
