from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        When an Image object is saved, if the slug field doesn’t have a value, the slugify() function is used
        to automatically generate a slug from the title field of the image. The object is then saved. By generating
        slugs automatically from the title, users won’t have to provide a slug when they share images
        on our website.
        """
        if not self.slug: # English --> If there is no slug, Hindi --> agar self.slug nahi hai.
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

