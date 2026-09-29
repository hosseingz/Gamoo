from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(
        max_length=255,
        unique=True,
        allow_unicode=True,
        verbose_name=_("Slug")
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_("Author")
    )
    content = models.TextField(verbose_name=_("Content"))
    cover_image = models.ImageField(
        upload_to='blog/covers/',
        blank=True,
        null=True,
        verbose_name=_("Cover Image")
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status")
    )
    reading_time = models.PositiveSmallIntegerField(
        default=1,
        help_text=_("Estimated reading time in minutes"),
        verbose_name=_("Reading Time")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self) -> str:
        return self.title
