from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .models import FavoriteJoke

def index(request):
    categories = ["animal", "career", "celebrity", "dev", "explicit", "fashion", "food", "history", "money", "movie", "music", "political", "religion", "science", "sport", "travel"]
    joke = "Clique em obter piada para ver uma piada do Chuck Norris."
    favorites = FavoriteJoke.objects.all()

    if request.method == 'GET' and 'category' in request.GET:
        category = request.GET['category']
        if category == 'random':
            response = requests.get('https://api.chucknorris.io/jokes/random')
        else:
            response = requests.get(f'https://api.chucknorris.io/jokes/random?category=' + category)
        if response.status_code == 200:
            joke = response.json().get('value')

    return render(request, 'chucknorris/index.html', {'categories': categories, 'joke': joke, 'favorites': favorites})

def get_joke(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        category = request.GET.get('category', 'random')
        if category == 'random':
            response = requests.get('https://api.chucknorris.io/jokes/random')
        else:
            response = requests.get(f'https://api.chucknorris.io/jokes/random?category={category}')
        if response.status_code == 200:
            joke = response.json().get('value')
            return JsonResponse({'joke': joke}, status=200)
    return JsonResponse({'error': 'Erro ao obter piada'}, status=400)

def save_favorite(request):
    if request.method == "POST":
        joke = request.POST.get('joke')
        if joke:
            favorite = FavoriteJoke(joke=joke)
            favorite.save()
            return redirect('index')
    return redirect('index')

def remove_favorite(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        import json
        data = json.loads(request.body)
        joke_id = data.get('id')
        try:
            favorite = FavoriteJoke.objects.get(id=joke_id)
            favorite.delete()
            return JsonResponse({'success': True})
        except FavoriteJoke.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Piada não encontrada.'})
    return JsonResponse({'success': False, 'error': 'Requisição inválida.'})
