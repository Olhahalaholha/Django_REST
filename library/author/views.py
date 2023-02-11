from django.shortcuts import render, redirect, get_object_or_404 
from django.views import generic 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import  DeleteView
from django.urls import reverse_lazy

from .models import Author
from book.models import Book
from .forms import AuthorForm
# Create your views here.

class AuthorsList(generic.View, LoginRequiredMixin):
    
    def get(self, *args, **kwargs):
        request = self.request 
        if request.user.role != 1:
            messages.warning(request, "You have no permissions to view this page.")
            return redirect('/')
        else:
            return render(request, 'author/list.html', {'authors': Author.objects.all()})
        
        
class AddAuthor(generic.View, LoginRequiredMixin):
    
    def get(self, *args, **kwargs):
        request = self.request 

        if request.user.role != 1:
            messages.warning(request, "You have no permissions to view this page.")
            return redirect('/')
        else:
            form= AuthorForm()
            context = {
                'form': form,
            }
            return render(request, 'author/create_form.html', context)
        
    def post(self, *args, **kwargs):    
        request = self.request 
        form = AuthorForm(request.POST)
        if form.is_valid():

            author_data = {
                'name': form.cleaned_data['name'],
                'surname': form.cleaned_data['surname'],
                'patronymic': form.cleaned_data['patronymic']
            }
        
            book_ids = form.cleaned_data['books']      
            books = Book.objects.filter(id__in=book_ids)
            form.save()

            author_obj = Author.objects.create(**author_data)
            author_obj.books.set(books)
            messages.success(request, f"""{author_data['surname']} {author_data['name']}
                                      {author_data['patronymic']} has been added to 
                                      authors! Check it out!""")
        return redirect('authors:all')
        
        
@login_required 
def delete_author(request, author_id):
    if request.user.role != 1:
        messages.warning(request, "You have no permissions for this action.")
        return redirect('/')
    author_obj = get_object_or_404(Author, id=author_id)
    author_obj.delete()
    messages.success(request, f"{author_obj.name}(id={author_obj.id}) has been deleted.")
    return redirect('authors:all')
    