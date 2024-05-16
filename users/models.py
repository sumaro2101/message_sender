from django.db import models

# Create your models here.


class NavBarList(models.Model):
    """Пункты навигации главного меню

    Отношеня users:NavBarList
    """    
    
    nav_name = models.CharField(max_length=50, verbose_name='пункт навигации', help_text='пункт навигации')
    slug = models.CharField(max_length=50, unique=True, verbose_name='адресс')
    
    def __str__(self) -> str:
        return self.nav_name

  
    class Meta:
        verbose_name = 'пункты'
        verbose_name_plural = 'пунк навигации'
        ordering = ['pk']
    
    
class Sublist(models.Model):
    """Под категории главного меню

    Отношеня users:Sublist
    """    
    
    nav_main = models.ForeignKey("users.NavBarList", verbose_name='под пункты навигации', on_delete=models.CASCADE)
    nav_sub_name = models.CharField(max_length=50, verbose_name='под пункт навигации', help_text='под пункт навигации')
    slug = models.CharField(max_length=50, unique=True, verbose_name='адресс')
    
    def __str__(self) -> str:
        return self.nav_sub_name
    
    class Meta:
        verbose_name = 'пункты'
        verbose_name_plural = 'под пункты навигации'
    