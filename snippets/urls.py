from django.urls import path
from .views import (
    SnippetAdd,
    SnippetEdit,
    SnippetDelete,
    SnippetDetails,
    UserSnippets,
    
    Login,
    Logout,
    Index,
)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('snippets/add/', SnippetAdd.as_view(), name='snippet_add'),
    path('snippets/edit/<int:id>/', SnippetEdit.as_view(), name='snippet_edit'),
    path('snippets/delete/<int:id>/', SnippetDelete.as_view(), name='snippet_delete'),
    path('snippets/<int:snippet_id>/', SnippetDetails.as_view(), name='snippet_detail'),
    path('user/<str:username>/', UserSnippets.as_view(), name='user_snippets'),

]