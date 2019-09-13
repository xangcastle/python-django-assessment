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
            self.object = Movie.objects.get(id=self.kwargs.get('id'))
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('movies:index'))


class MovieCreateView(CreateView):
    """Create a new movie."""
    fields = ('__all__')
    model = Movie
    template_name = 'movies/movie_form.html'
    slug_field = 'id'
    success_message = 'The movie created successfully'
    error_message = 'The creation has failed'

    def form_valid(self, form):
        response = super(MovieCreateView, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def form_invalid(self, form):
        response = super(MovieCreateView, self).form_invalid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data


class MovieUpdateView(UpdateView):
    """Update the requested movie."""
    model = Movie
    fields = ('__all__')
    pk_url_kwarg = 'id'

    success_message = 'The movie updated successfully'
    error_message = 'The update has failed'

    def form_valid(self, form):
        response = super(MovieUpdateView, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def form_invalid(self, form):
        response = super(MovieUpdateView, self).form_invalid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data


class MovieDeleteView(DeleteView):
    """Delete the requested movie."""
    model = Movie
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        url = reverse_lazy('movies:index')
        try:
            Movie.objects.get(id=self.kwargs.get('id')).delete()
            messages.add_message(request, messages.SUCCESS, 'The movie deleted successfully')
            return redirect(url)
        except:
            messages.add_message(request, messages.ERROR, 'The deletion has failed.')
            return redirect(url)
