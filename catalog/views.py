
from datetime import datetime,timedelta
from typing import Iterable
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.forms import RenewBookModelForm
from catalog.models import CartItem

#from forms import RenewBookForm



from .models import Book, Author, BookInstance, Genre, Language

def index(request):
    """View function for home page"""

    #Generate counts of some of the main books
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    last_books = Book.objects.order_by('-id')[:5]

    #Avaiable books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default.
    num_authors = Author.objects.count()


    #number of visits to this view, ass counted in the session variable
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'last_books': last_books,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits' : num_visits,
    }

    #Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def aboutus(request):
    context = {
        
    }
    return render(request, 'aboutus.html', context=context)

class BookListView(generic.ListView):
    model= Book
    context_object_name = 'book_list'
    template_name='book_list.html'
    paginate_by = 10
    def get_queryset(self):
        author_id = self.request.GET.get('author')
        queryset = super().get_queryset()
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_list'] = Author.objects.all()
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book-detail.html'
    

class AuthorListView(generic.ListView):
    model= Author
    content_object_name = 'author_list'
    template_name='author_list.html'
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todos los libros del autor
        books_with_author = Book.objects.filter(author=self.object) # type: ignore

        context['books'] = books_with_author
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user"""
    permission_required = ('catalog.can_mark_returned')
    model = BookInstance
    template_name = 'bookinstance_list_all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    import datetime
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('allborrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2020'}
    
class AuthorUpdate(UpdateView):
    model = Author
    fields= '__all__'
    
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author_list')
    
class BookCreate(CreateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    initial = {'Language':'English'}
    
class BookUpdate(UpdateView):
    model = Book
    fields= '__all__'
    
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Obtén una instancia disponible del libro
        book_instance = get_object_or_404(BookInstance, book=book, status='a')

        # Cambia el estado a 'On loan'
        book_instance.status = 'o'
        book_instance.due_back = datetime.now() + timedelta(weeks=3)
        book_instance.borrower = request.user
        book_instance.save()

        # Agrega el libro al carrito
        cart_item, created = CartItem.objects.get_or_create(book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return render(request, 'success.html', {'book_instance': book_instance})


class CartView(View):
    def get(self, request):
        cart_items = CartItem.objects.all()
        total_price = sum(item.get_total_price() for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    
    
