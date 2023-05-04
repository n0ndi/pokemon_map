import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import *


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entity = PokemonEntity.objects.filter(appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemon_entity:
        if not pokemon.pokemon.image:
            continue
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url if pokemon.image else None),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_entities = pokemon.entities.filter(appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    # for pokemon in pokemon_entity:
    #     if pokemon['pokemon_id'] == int(pokemon_id):
    #         requested_pokemon = pokemon
    #         break
    # else:
    #     return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        if not pokemon_entity.pokemon.image:
            continue
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    try:
        pokemon.next_evolution = pokemon.next_evolutions.all()[0]
    except IndexError:
        pokemon.next_evolution = None
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
