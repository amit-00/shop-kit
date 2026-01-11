from django.db import models

from apps.common.model_utils import TimestampedModel
from apps.identity.models import User

# Create your models here.
class Shop(TimestampedModel):
    class Theme(models.TextChoices):
        LIGHT = 'light'
        DARK = 'dark'
        CUPCAKE = 'cupcake'
        BUMBLEBEE = 'bumblebee'
        EMERALD = 'emerald'
        CORPORATE = 'corporate'
        SYNTHWAVE = 'synthwave'
        RETRO = 'retro'
        CYBERPUNK = 'cyberpunk'
        VALENTINE = 'valentine'
        HALLOWEEN = 'halloween'
        GARDEN = 'garden'
        FOREST = 'forest'
        AQUA = 'aqua'
        LOFI = 'lofi'
        PASTEL = 'pastel'
        FANTASY = 'fantasy'
        WIREFRAME = 'wireframe'
        BLACK = 'black'
        LUXURY = 'luxury'
        DRACULA = 'dracula'
        CMYK = 'cmyk'
        AUTUMN = 'autumn'
        BUSINESS = 'business'
        ACID = 'acid'
        LEMONADE = 'lemonade'
        NIGHT = 'night'
        COFFEE = 'coffee'
        WINTER = 'winter'
        DIM = 'dim'
        NORD = 'nord'
        SUNSET = 'sunset'
        CARAMELLATTE = 'caramellatte'
        ABYSS = 'abyss'
        SILK = 'silk'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    support_email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to='shops/logos/', null=True, blank=True)
    theme = models.CharField(max_length=255, choices=Theme.choices, default=Theme.LIGHT)
    content = models.JSONField(null=True, blank=True)
    custom_domain = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['user']),
        ]


class Policy(TimestampedModel):
    class Type(models.TextChoices):
        RETURN_POLICY = 'return_policy'
        PRIVACY_POLICY = 'privacy_policy'
        TERMS_OF_SERVICE = 'terms_of_service'
        SHIPPING_POLICY = 'shipping_policy'
        PAYMENT_POLICY = 'payment_policy'
        CANCELLATION_POLICY = 'cancellation_policy'
        REFUND_POLICY = 'refund_policy'
        WARRANTY_POLICY = 'warranty_policy'
        WARRANTY_POLICY = 'warranty_policy'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='policies')
    type = models.CharField(max_length=255, choices=Type.choices, default=Type.RETURN_POLICY)
    content = models.TextField(null=True, blank=True)


class Product(TimestampedModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['shop']),
        ]


class ProductImage(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shops/products/', null=True, blank=True)
    position = models.IntegerField(default=0)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.position}"
        
    class Meta:
        indexes = [
            models.Index(fields=['product']),
        ]


class Price(TimestampedModel):
    class Currency(models.TextChoices):
        USD = 'usd'
        CAD = 'cad'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    amount = models.IntegerField()
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

