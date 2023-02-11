"""
Views for book
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from author.models import Author
from order.models import Order
from django.http import HttpResponseForbidden
from authentication.models import CustomUser
from authentication.forms import SearchUserById


@login_required()
def view_set(request):
    """All books view"""
    filter_data = dict()
    books = Book.objects.all()

    if request.GET.get('author'):
        try:
            filter_data['author'] = int(request.GET.get('author'))
        except ValueError as e:
            print(e)
        else:
            books = books.filter(authors__in=[filter_data['author']])
    if request.GET.get('book'):
        try:
            filter_data['book'] = int(request.GET.get('book'))
        except ValueError as e:
            print(e)
        else:
            books = books.filter(pk=filter_data['book'])

    authors = Author.objects.filter(books__in=books).distinct()

    return render(request, 'book/all.html', {'books': books,
                                             'authors': authors,
                                             'filter_data': filter_data})


@login_required()
def detail_view(request, book_id):
    """Detail book view"""
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/detail.html', {'book': book})


@login_required()
def view_books_by_user(request):
    """All books by user view - only for librarian"""
    if request.user.role != 1:
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = SearchUserById()
        return render(request, 'book/book_by_user.html', {'search_form': form})

    if request.method == 'POST':
        form = SearchUserById(request.POST)
        res = ''
        search_query = ''
        if form.is_valid():
            search_query = form.cleaned_data['user_id']
            res = Order.objects.filter(user__pk=search_query)\
                .select_related('book').order_by('-end_at')

        return render(request, 'book/book_by_user.html',
                      {'search_query': search_query,
                       'orders': res,
                       'search_form': form})
