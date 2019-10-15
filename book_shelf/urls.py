from django.urls import path#, include, my_loan_book
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('author_index/', views.author_index, name='author_index'),
        #List and Detail views
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genres/<int:pk>', views.Book_by_Genre, name='genre-detail'),
    path('languages/', views.LanguageListView.as_view(), name='languages'),
    path('languages/<int:pk>', views.LanguageDetailView.as_view(), name='language-detail'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('brbooks/', views.LoanedBooks_ByUserListView.as_view(), name='br-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
        #Create, Update and Delete views
    path('bookinstance/(?P<pk>\d+)/$', views.BookInstanceUpdate.as_view(), name='bookinstance_update'),
    path(r'^bookinstance/(?P<pk>\d+)/$', views.create_book_instances, name='bookinstance_create'),
    path('author/create/', views.AuthorCreate, name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('genre/create/', views.GenreCreate, name='genre_create'),
    path('genre/<int:pk>/update/', views.GenreUpdate.as_view(), name='genre_update'),
    path('genre/<int:pk>/delete/', views.GenreDelete.as_view(), name='genre_delete'),
    path('language/create/', views.LanguageCreate, name='language_create'),
    path('language/<int:pk>/update/', views.LanguageUpdate.as_view(), name='language_update'),
    path('language/<int:pk>/delete/', views.LanguageDelete.as_view(), name='language_delete'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
        #Django Account view       #user views
    path('book/author/', views.book_authors, name='author'),
    path('book/stores/', views.book_stores, name='stores'),
    path(r'^stores/(?P<pk>\d+)/$', views.book_copies, name='copies'),
    path('applyforbook/<uuid:pk>/qeues/', views.applied_for_Book, name='qeues'),
    path('book/<uuid:pk>/approval/', views.BookLoanApproval, name='approval'),
    path('book/qeuing/', views.LoanedBooks_On_Qeue.as_view(), name='qeuing'),
    path('my_loan_book/', views.my_loan_book, name='my_loan_book'),
    path('book/<uuid:pk>/renew_qeues/', views.applied_for_Book_renew, name='renew_qeues'),
    path('book/renew/', views.renew_loan_book, name='renew_approval'),
    #path('book_copies/(?P<pk>\d+)/$', views.applied_for_Book_Intances, name='book_copies'),
]
