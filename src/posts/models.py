from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save                                   # pour la création des signaux
from django.urls import reverse
from .utils import unique_slug_generator                                        # Slug generator


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug  = models.SlugField(null=True, blank=True, editable=False, verbose_name="Slug") #necesite une instance title.
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)         # everytime
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)           # initialy

    def __str__(self):                                                          # python 3
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"slug": self.slug})

### Signals de création des slugs
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Post)
