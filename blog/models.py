from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class PostComment(models.Model):
    """Модель комментария к посту
    """
    post = models.ForeignKey('Posts',
                             verbose_name='имя поста',
                             on_delete=models.CASCADE
                             )
    parent = models.ForeignKey("self",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True
                               )
    user_name = models.ForeignKey(get_user_model(),
                                  related_name='postcomment',
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True,
                                  verbose_name='имя пользователя'
                                  )
    image = models.ImageField(upload_to='post_users/%Y/%m/%d/',
                              blank=True,
                              null=True,
                              verbose_name='картинка'
                              )
    text = models.TextField(verbose_name='описание',
                            blank=True,
                            null=True
                            )
    time_published = models.DateTimeField(auto_now_add=True,
                                          verbose_name='дата публикации'
                                          )
    time_edit = models.DateTimeField(auto_now=True,
                                     verbose_name='дата измененения'
                                     )
    is_edit = models.BooleanField(default=False)
    text_to_edit = models.CharField(max_length=50,
                                    default='Изменено:'
                                    )
    likes = models.IntegerField(verbose_name='лайки',
                                default=0
                                )
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.time_published}-{self.is_published}-{self.likes}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-time_published']


class Posts(models.Model):
    """Модель поста
    """
    title = models.CharField(max_length=200,
                             verbose_name='название поста'
                             )
    name_user = models.ForeignKey(get_user_model(),
                                  related_name='posts',
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True,
                                  verbose_name='имя пользователя'
                                  )
    image = models.ImageField(upload_to='posts/%Y/%m/%d/',
                              blank=True,
                              null=True,
                              verbose_name='картинка'
                              )
    description = models.TextField(verbose_name='описание')
    slug = models.SlugField(unique=True,
                            max_length=200
                            )
    views = models.PositiveIntegerField(verbose_name='просмотры',
                                        default=0,
                                        editable=False
                                        )
    likes = models.IntegerField(verbose_name='лайки',
                                default=0
                                )
    time_published = models.DateTimeField(auto_now_add=True,
                                          verbose_name='дата публикации'
                                          )
    time_edit = models.DateTimeField(blank=True,
                                     null=True,
                                     verbose_name='дата измененения'
                                     )
    is_edit = models.BooleanField(default=False)
    text_to_edit = models.CharField(max_length=50,
                                    default='Изменено:'
                                    )
    comment_count = models.IntegerField(default=0,
                                        verbose_name='количество комментариев'
                                        )
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.title}-{self.slug}'

    def get_absolute_url(self):
        return reverse("blog:posts")

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-time_published']
