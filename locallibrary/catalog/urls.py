<<<<<<< HEAD
from django.urls import include, path


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author_list', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksListView.as_view(),name='allborrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
=======
from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
>>>>>>> 5d243dd (PrimerPush)
    
=======
    path('', views.index, name='index'),
>>>>>>> 48ddd71 (commit del index html)
]