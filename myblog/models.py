from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.cache.utils import make_template_fragment_key
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from reading_statistics.models import ReadDetail


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-create_time']

    # Delete cache when update blog.
    def save(self, *args, **kwargs):
        cache.delete(make_template_fragment_key('blog_content', [self.pk]))
        super().save(*args, **kwargs)
