from django.db import models

class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    image = models.ImageField("Картинка", blank=True, null=True)
    description = models.CharField("Описание", max_length=200, blank=True)
    title_en = models.CharField("Имя на английском", max_length=200, blank=True)
    title_jp = models.CharField("Имя на японском", max_length=200, blank=True)
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционирует',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities", verbose_name = "Покемон")
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField("Время появления")
    disappeared_at = models.DateTimeField("Время исчезновения ")
    level = models.IntegerField("Уровень", blank=True, null=True)
    health = models.IntegerField("Здоровье", blank=True, null=True)
    strength = models.IntegerField("Сила", blank=True, null=True)
    defence = models.IntegerField("Защита", blank=True, null=True)
    stamina = models.IntegerField("Энергия", blank=True, null=True)

    def __str__(self):
        return f"{self.id}.{self.pokemon.title}"

    class Meta:
        verbose_name = "Существо"
        verbose_name_plural = "Существа"

