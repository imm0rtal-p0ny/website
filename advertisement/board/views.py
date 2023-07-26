import os
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Board, Division, delete_photos_except_default, DEFAULT_BOARD_PHOTO, \
    DEFAULT_BOARD_PHOTO_PAGE, DEFAULT_BOARD_PHOTO_ICON
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from . import forms
from user.models import CustomUser
from PIL import Image, ImageOps


def create_mini_size_photo(image_path, size):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    name, extension = os.path.splitext(image_path)
    image_path_mini = f'{name}{extension}'
    image = Image.open(image_full_path)
    image.thumbnail(size)
    padded_image = ImageOps.pad(image, size)
    buffer = BytesIO()
    padded_image.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue())

    return image_path_mini.split('/')[-1], image_file


class BoardListView(ListView):
    template_name = 'board/board_list.html'
    model = Board
    paginate_by = 10

    def filters_queryset(self, queryset):
        form = forms.FilterForm(self.request.GET)
        if form.is_valid():
            if region_name := form.cleaned_data.get('region'):
                queryset = queryset.filter(region__name=region_name)
            if condition_name := form.cleaned_data.get('condition'):
                queryset = queryset.filter(condition__name=condition_name)
            if division_name := form.cleaned_data.get('division'):
                queryset = queryset.filter(division__name=division_name)

            return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        form = forms.SearchForm(self.request.GET)
        queryset = self.filters_queryset(queryset)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data.get('search'))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        divisions = Division.objects.all()
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['search_form'] = forms.SearchForm(self.request.GET)
        context_data['divisions'] = divisions
        context_data['filter_form'] = forms.FilterForm(self.request.GET)
        context_data['clear_url'] = self.request.build_absolute_uri().split('?')[0]
        return context_data


class BoardDetailView(DetailView):
    template_name = 'board/board_detail.html'
    model = Board

    def get_object(self, queryset=None):
        board = super().get_object(queryset)
        board.view_count += 1
        board.save()
        return board


class BoardCreateView(CreateView):
    model = Board
    fields = [
        'photo',
        'name',
        'description',
        'price',
        'count',
        'region',
        'division',
        'condition',
        'status',
    ]
    template_name = 'board/create_board.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        board = form.save(commit=False)
        board.user = self.request.user
        return super().form_valid(form)

    def get(self, request,  *args, **kwargs):
        get_return = super().get(request,  *args, **kwargs)
        if not request.user.is_authenticated:
            return redirect('authorization')
        else:
            if not request.user.is_authorized:
                return redirect('verification')

        return get_return

    def post(self, request, *args, **kwargs):
        post_return = super().post(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return redirect('authorization')
        else:
            if not request.user.is_authorized:
                return redirect('verification')

        return post_return


class BoardUpdateView(UpdateView):
    model = Board
    template_name = 'board/create_board.html'
    form_class = forms.BoardUpdateForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        result = super().get_object(queryset=queryset)
        self.old_photo = result.photo
        return result

    def get(self, request,  *args, **kwargs):
        get_return = super().get(request,  *args, **kwargs)
        if not request.user.is_authenticated:
            return redirect('authorization')
        else:
            if not request.user.is_authorized:
                return redirect('verification')
        if not self.object.user == self.request.user:
            return redirect('home')
        return get_return

    def post(self, request, *args, **kwargs):
        post_return = super().post(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return redirect('authorization')
        else:
            if not request.user.is_authorized:
                return redirect('verification')

        return post_return

    def form_valid(self, form):
        self.object.update_photo(self.old_photo, form.cleaned_data.get('clear_photo'))

        return super().form_valid(form)


class DivisionBoardListView(ListView):
    template_name = 'board/division_list.html'
    model = Division

    def filters_queryset(self, queryset):
        form = forms.FilterForm(self.request.GET)
        if form.is_valid():
            if region_name := form.cleaned_data.get('region'):
                queryset = queryset.filter(region__name=region_name)
            if condition_name := form.cleaned_data.get('condition'):
                queryset = queryset.filter(condition__name=condition_name)
            if division_name := form.cleaned_data.get('division'):
                queryset = queryset.filter(division__name=division_name)

            return queryset

    def get_queryset(self):
        division = get_object_or_404(Division, name=self.kwargs.get('name'))
        form = forms.SearchForm(self.request.GET)
        queryset = division.board_set.all()
        queryset = self.filters_queryset(queryset)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data.get('search'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['search_form'] = forms.SearchForm()
        context_data['filter_form'] = forms.FilterForm(self.request.GET)
        context_data['clear_url'] = self.request.build_absolute_uri().split('?')[0]

        return context_data


class UserBoardListView(ListView):
    template_name = 'board/user_board_list.html'
    model = CustomUser

    def filters_queryset(self, queryset):
        form = forms.FilterForm(self.request.GET)
        if form.is_valid():
            if region_name := form.cleaned_data.get('region'):
                queryset = queryset.filter(region__name=region_name)
            if condition_name := form.cleaned_data.get('condition'):
                queryset = queryset.filter(condition__name=condition_name)
            if division_name := form.cleaned_data.get('division'):
                queryset = queryset.filter(division__name=division_name)

            return queryset

    def get_queryset(self):
        user_board = get_object_or_404(CustomUser, pk=self.kwargs.get('pk'))
        queryset = user_board.board_set.all()
        queryset = self.filters_queryset(queryset)
        form = forms.SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data.get('search'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['search_form'] = forms.SearchForm(self.request.GET)
        context_data['filter_form'] = forms.FilterForm(self.request.GET)
        context_data['clear_url'] = self.request.build_absolute_uri().split('?')[0]

        return context_data


def delete_board(request, pk):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.pk)
        board = Board.objects.get(pk=pk)
        if user == board.user:
            board.delete()

            print(board, 111)

    return redirect('home')




