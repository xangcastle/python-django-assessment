# -*- coding: utf-8 -*-

"""Movies views."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .models import Movie


class MovieListView(ListView):
    """Show all movies."""
    model = Movie


class MovieDetailView(DetailView):
    """Show the requested movie."""
    model = Movie

    def get(self, request, *args, **kwargs):
        try:
            self.object = Movie.objects.get(id=self.kwargs.get('pk'))
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('movies:index'))


class MovieCreateView(CreateView):
    """Create a new movie."""
    fields = ('__all__')
    model = Movie
    template_name = 'movies/movie_form.html'

    def post(self, request, *args, **kwargs):
        formmodel = self.get_form_class()
        form = formmodel(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'The movie has been successfully created!')
        else:
            messages.add_message(request, messages.ERROR, 'The creation has failed.')
        return super(MovieCreateView, self).post(request, args, kwargs)


class MovieUpdateView(UpdateView):
    """Update the requested movie."""
    model = Movie
    fields = ('__all__')

    def post(self, request, *args, **kwargs):
        formmodel = self.get_form_class()
        form = formmodel(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'The movie has been successfully updated!')
        else:
            messages.add_message(request, messages.ERROR, 'The update has failed.')
        return super(MovieUpdateView, self).post(request, args, kwargs)


class MovieDeleteView(DeleteView):
    """Delete the requested movie."""
    model = Movie

    def post(self, request, *args, **kwargs):
        url = reverse_lazy('movies:index')
        try:
            Movie.objects.get(id=self.kwargs.get('pk')).delete()
            messages.add_message(request, messages.SUCCESS, 'The movie has been successfully deleted!')
            return redirect(url)
        except:
            messages.add_message(request, messages.ERROR, 'The deletion has failed.')
            return redirect(url)