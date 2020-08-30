from django.urls import path

from . import views
app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.article, name="entry"),
    path("editor/newwiki", views.newwiki, name="newwiki"),
    path("editor/edit", views.edit, name="editEntry")

]
