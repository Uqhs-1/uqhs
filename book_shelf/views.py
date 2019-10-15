from django.shortcuts import render, redirect
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import formset_factory
from book_shelf.forms import RenewBookForm, BookInstanceForm, BookRenew, Author_form, Genre_form, Book_form
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from book_shelf.models import Author
from book_shelf.models import Book, BookInstance, Genre, Language
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
 
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    fiction_books = Book.objects.filter(genre__name__icontains='Fiction').count()
    booktitle_with_th = Book.objects.filter(title__icontains='th').count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='Available').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'fiction_books': fiction_books,
        'booktitle_with_th': booktitle_with_th,
        'num_authors': num_authors,
        'num_visits': num_visits,
        }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def author_index(request):
    book_by_author = Book.objects.filter(author__last_name__icontains='Rowan')
    context = {
        'author': book_by_author,
        }
    print(context)
    #return render(request, 'author_index.html', context=context)
    return render(request, 'book_shelf/author_index.html', {'author': book_by_author})
from django.views import generic
#######################model_views####################################################
class BookListView(generic.ListView):
    model = Book
    paginate_by = 60#pagenation
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 60
    
class AuthorDetailView(generic.DetailView):
    model = Author

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 60
    
class GenreDetailView(generic.DetailView):
    model = Genre
    
class LanguageListView(generic.ListView):
    model = Language
    paginate_by = 60
class LanguageDetailView(generic.DetailView):
    model = Language
    
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='book_shelf/bookinstance_list_borrowed_user.html'
    paginate_by = 60
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
class LoanedBooks_ByUserListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='book_shelf/bookinstance_list_borrowed_to_users.html'
    paginate_by = 60#users
    permission_required = 'book_shelf.can_mark_returned'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='On loan').order_by('due_back')

  
#######################BOOK_RENEWER####################################################
@permission_required('book_shelf.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.renew = 'Okyed'
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('renew_approval') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_shelf/book_renew_librarian.html', context)



#######################UTHORS_BOOK####################################################
def AuthorCreate(request):
    if request.method == 'POST':
        form = Author_form(request.POST)
        if form.is_valid():
            #author = Author(first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], date_of_birth = form.cleaned_data['date_of_birth'], date_of_death = form.cleaned_data['date_of_death'])
            form.save()
            return redirect('authors')
    else:
        form = Author_form()
    return render(request, 'book_shelf/new_author.html', {'form': form})   


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'book_shelf.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'book_shelf.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')
    
    
def GenreCreate(request):
    if request.method == 'POST':
        form = Genre_form(request.POST)
        if form.is_valid():
            Gen = Genre(name = form.cleaned_data['name'])
            Gen.save()
            return redirect('genres')
    else:
        form = Genre_form()
    return render(request, 'book_shelf/new_genre.html', {'form': form})   

class GenreUpdate(UpdateView):
    model = Genre
    fields = ['name']

class GenreDelete(DeleteView):
    model = Genre
    success_url = reverse_lazy('genres')    

    
def LanguageCreate(request):
    if request.method == 'POST':
        form = Genre_form(request.POST)
        if form.is_valid():
            Lang = Language(name = form.cleaned_data['name'])
            Lang.save()
            return redirect('languages')
    else:
        form = Genre_form()
    return render(request, 'book_shelf/new_language.html', {'form': form}) 
    
class LanguageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'book_shelf.can_mark_returned'
    model = Language
    fields = ['name']

class LanguageDelete(DeleteView):
    model = Language
    success_url = reverse_lazy('languages')
#######################BOOK####################################################   

def BookCreate(request):
    if request.method == 'POST':
        form = Book_form(request.POST)
        if form.is_valid():
            #book = Book(title = form.cleaned_data['title'], author = form.cleaned_data['author'], summary = form.cleaned_data['summary'], isbn = form.cleaned_data['isbn'], genre = form.cleaned_data['genre'], language = form.cleaned_data['language'])
            form.save()
            return redirect('books')
    else:
        form = Book_form()
    return render(request, 'book_shelf/new_book.html', {'form': form})


@permission_required('book_shelf.can_mark_returned')
def create_book_instances(request, pk):
    BookFormset = formset_factory(BookInstanceForm, extra=int(Book.objects.get(pk=pk).no_of_copy))
    template_name = 'book_shelf/create_book_instance.html'
    heading_message = 'Create Book Multiple Instance'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('imprint')
                status = form.cleaned_data.get('status')
                # save book instance
                if name:
                    BookInstance(imprint=name, book=Book.objects.get(pk=pk), status= status).save()
            # once all books are saved, redirect to book list view
            return redirect('copies', pk=pk)
    return render(request, template_name, {'formset': formset, 'heading': heading_message,})


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    success_url = reverse_lazy('stores')
    fields = ['id',	'imprint',	'due_back',	'borrower',	'renew',	'status']
    permission_required = 'book_shelf.can_mark_returned'
    
class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'book_shelf.can_mark_returned'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', 'no_of_copy']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class LoanedBooks_On_Qeue(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='book_shelf/bookinstance_list_2_2.html'
    paginate_by = 60#users
    permission_required = 'book_shelf.can_mark_returned'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='Available').order_by('id') 

#@login_required
def my_loan_book(request):
    if request.user.is_authenticated:
        book_instance = BookInstance.objects.filter(borrower = request.user, status__exact='On loan').order_by('id')
    else:
            return redirect('home')
    return render(request, 'book_shelf/my_loan_book.html', {'book_instance' : book_instance})

def book_stores(request):
    book_stores = Book.objects.all().order_by('title')
    return render(request, 'book_shelf/book_stores.html', {'book_stores' : book_stores})

def book_authors(request):
    book_authors = Author.objects.all().order_by('first_name')
    return render(request, 'book_shelf/book_authors.html', {'book_authors' : book_authors})

def book_copies(request, pk):
    book_copies = BookInstance.objects.filter(book_id = pk).order_by('status')
    return render(request, 'book_shelf/book_copies.html', {'book_copies' : book_copies})

@login_required
def applied_for_Book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.borrower = request.user
    book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
    book_instance.save()
    return HttpResponseRedirect(reverse('stores'))

def Book_by_Genre(request, pk):
    book_by_genre = Book.objects.filter(genre__exact = get_object_or_404(Genre, pk=pk))
    return render(request, 'book_shelf/book_by_genre.html', {'book_by_genre' : book_by_genre})


@login_required
def applied_for_Book_renew(request, pk):
    book_renew = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = BookRenew(request.POST)
        if form.is_valid():
            book_renew.renew = form.cleaned_data['renewal_date']
            book_renew.save()
            return HttpResponseRedirect(reverse('my_loan_book'))
    else:
        form = BookRenew()
    return render(request, 'book_shelf/book_renew.html', {'book_renew' : book_renew, 'form': form,})


@login_required
def renew_loan_book(request):
    book_renew = BookInstance.objects.filter(renew__exact='renew').order_by('id')
    return render(request, 'book_shelf/renew_book.html', {'book_renew' : book_renew})

@permission_required('book_shelf.can_mark_returned')
def BookLoanApproval(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = 'On loan'
    book_instance.save()
    return HttpResponseRedirect(reverse('qeuing') )