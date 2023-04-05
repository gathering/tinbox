from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('screens', views.list_screens, name='screens'),
    path('slideshows', views.list_slideshows, name='slideshows'),
    path('slideshow/<int:id>', views.edit_slideshow, name='slideshow'),
    path('slide/<int:id>', views.edit_slide, name='slide'),
    path('slide/new/<int:slideshow_id>/template/<int:template_id>', views.new_slide, name='new_slide'),
    path('slide/<int:id>/delete', views.delete_slide, name='delete_slide'),
    path('slide_templates', views.list_slide_templates, name='slide_templates'),
    path('view/slide/<int:id>', views.view_slide, name='view_slide'),
    path('view/screen/<int:id>', views.view_screen, name='view_screen'),
    path('api/get/screen/<int:id>', views.api_get_screen, name='api_get_screen'),
    path('assets', views.list_assets, name='list_assets'),
    path('asset/new', views.new_asset, name="new_asset"),
    path('asset/<int:id>', views.view_asset, name="view_asset"),
    path('asset/<int:id>/delete', views.delete_asset, name="delete_asset"),
]