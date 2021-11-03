from random import randint
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from model_utils import Choices
from extensions.utils import jalali_converter
from account.models import MyUser
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils.text import slugify


# my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name='خانواده')
    title = models.CharField(max_length=100, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(max_length=100, verbose_name='انتشار')
    position = models.PositiveIntegerField(verbose_name='شماره')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = ' دسته بندی ها '
        ordering = ['position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


def random_string():
    return str(randint(10000, 99999))


class Article(models.Model):
    STATUS_CHOICES = (
        ('p', 'منتشر شده'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    TYPE_CHOICES = Choices('-------', 'آپارتمان', 'خانه و ویلا', 'زمین/کلنگی', 'متفرقه', 'مسکونی', 'اداری و تجاری')
    CONTRACT_CHOICES = Choices('-------', 'اجاره', 'خرید')
    DIRECTION_CHOICES = Choices('-------', 'درب به ساختمان ', 'درب به حیاط ')
    CONDITIONS_CHOICES = Choices('-------', 'قابل تبدیل', 'معاوضه', 'مشارکتی', 'پیش فروش', 'وضعیت اداری', 'وام دار',
                                 'قدرالسهم', 'پاساژ', 'مال', 'باسازی شده',
                                 )
    COVERING_CHOICES = Choices('-------', 'دارد', 'فرش و موکت', 'کاشی و موزاییک', 'سنگ', 'سرامیک', 'بتنی', 'PVC',
                               'بامبو', 'پارکت و لمینت')
    COOLING_CHOICES = Choices('-------', 'دارد', 'کولر آبی', 'فن کويل', 'اسپلیت', 'داکت اسپلیت', 'کولر گازی')
    HEATING_CHOICES = Choices('-------', 'دارد', 'از کف', 'بخاری', 'شومینه', 'اسپلیت', 'داکت اسپلیت', 'فن کویل', 'پکیج')
    WATER_CHOICES = Choices('-------', 'دارد', 'آبگرمکن', 'پکیج', 'موتورخانه')
    CONSTRUCTION_CHOICES = Choices('-------', 'اسکلت بتن', 'شناژ', 'معمولی ساز','اسکلت فلزی')
    FRONTAGE_CHOICES = Choices('-------', 'نمای آجری', 'نمای کامپوزیت', 'نمای سنگ', 'نمای چوبی', 'نمای اتیکس',
                               'نمای سرامیکی', 'نمای شیشه ای', 'نمای مینرال', 'نما رومی', 'نانو نما ',
                               ' نمای کنیتکس')
    DOCUMENT_CHOICES = Choices('-------', 'سند مفروز', 'سند مشاع'
                               , 'سند شش دانگ', 'سند منگوله دار', 'سند تک برگ', 'سند اعیان', 'سند عرصه',
                               'سند وقفی', 'سند ورثه‌ای', 'سند المثنی', 'سند معارض', 'سند شورایی', 'سند وکالتی',
                               'سند بنچاق', 'سند رهنی', )
    ADVERTISER_CHOICES = Choices('شخصی', 'مشاور املاک')
    code = models.CharField(max_length=99999, default=random_string, blank=True, null=True, verbose_name='کد آگهی')
    title = models.CharField(max_length=300, verbose_name='عنوان آگهی')
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='آدرس سایت',
                            help_text='عنوان ادرس سایت بهتر است مانند عنوان آگهی باشد (به ازای هر فاصله - بزنید)')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    tags = TaggableManager(blank=True, verbose_name='املاک مرتبط', help_text='همان دسته بندی های انتخاب شده را بنویسید')
    description = RichTextField(blank=True, null=True, verbose_name='توضیحات',
                                help_text='در توضیحات آگهی به مواردی مانند شرایط اجاره، جزئیات و ویژگی‌های قابل توجه، '
                                          'امکانات ملک اشاره کنید.')

    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت',
                              help_text='وضعیت ملک ها را مشخص کنید')
    author = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL, related_name='articles', blank=True,
                               verbose_name='نماینده')
    property_contract = models.CharField(choices=CONTRACT_CHOICES, default=CONTRACT_CHOICES, max_length=20,
                                         verbose_name='نوع آگهی')
    property_type = models.CharField(choices=TYPE_CHOICES, default='-------', max_length=40, verbose_name='نوع ملک')

    unit_price = models.PositiveIntegerField(verbose_name='قیمت / ودیعه', null=True, blank=True)
    Deposit2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='اجاره',
                                           help_text='اگر نوع آگهی شما مربوط به خرید و فروش هست این قسمت را رها کنید')
    Deposit1 = models.BooleanField(verbose_name='رهن کامل', default=False,
                                   help_text='اگر نوع آگهی شما مربوط به خرید و فروش هست این قسمت را رها کنید')
    Agree_unit = models.BooleanField(verbose_name='قیمت توافقی', default=False)
    Special = models.BooleanField(verbose_name='ملک مفت', default=False)
    Special2 = models.BooleanField(verbose_name='در صفحه اول ملک مفت', default=False)
    bedrooms = models.PositiveIntegerField(default=0, null=False, verbose_name='تعداد اتاق')
    area = models.PositiveIntegerField(default=0, null=False, verbose_name='متراژ')
    foundation = models.PositiveIntegerField(default=0, null=False, blank=True, verbose_name='زیربنا')
    year_built = models.PositiveIntegerField(default=0, null=False, blank=True, verbose_name='سال ساخت')
    region = models.CharField(max_length=300, verbose_name='منطقه')
    address = models.CharField(max_length=20000, verbose_name='آٔدرس', blank=True)

    construction_contract = models.CharField(choices=CONSTRUCTION_CHOICES, default='-------', max_length=20,
                                             verbose_name='نوع ساخت', blank=True, null=True)
    document_contract = models.CharField(choices=DOCUMENT_CHOICES, default='-------', max_length=20,
                                         verbose_name='نوع سند', blank=True, null=True)
    conditions_contract = models.CharField(choices=CONDITIONS_CHOICES, default='-------', max_length=30,
                                           verbose_name='شرایط', blank=True, null=True)
    direction_contract = models.CharField(choices=DIRECTION_CHOICES, default='-------', max_length=20,
                                          verbose_name='جهت ساختمان', blank=True, null=True)
    frontage_contract = models.CharField(choices=FRONTAGE_CHOICES, default='-------', max_length=20,
                                         verbose_name='نمای ساختمان', blank=True, null=True)
    cooling_contract = models.CharField(choices=COOLING_CHOICES, default='-------', max_length=20,
                                        verbose_name='سیستم سرمایشی', blank=True, null=True)
    heating_contract = models.CharField(choices=HEATING_CHOICES, default='-------', max_length=20,
                                        verbose_name='سیستم گرمایشی', blank=True, null=True)
    water_contract = models.CharField(choices=WATER_CHOICES, default='-------', max_length=20,
                                      verbose_name='آب گرم', blank=True, null=True)
    covering_contract = models.CharField(choices=COVERING_CHOICES, default='-------', max_length=20,
                                         verbose_name='جنس کف', blank=True, null=True)
    Parking_lots = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='پارکینگ')
    floor = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='طبقه')
    advertiser = models.CharField(choices=ADVERTISER_CHOICES, default=ADVERTISER_CHOICES, max_length=30,
                                  verbose_name='آگهی دهنده')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن آگهی دهنده')
    full_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='نام و نام خانوادگی آگهی دهنده')
    thumbnail = models.ImageField(upload_to='image', verbose_name='عکس کاور و اصلی',
                                  help_text='این قسمت واجب است وارد کنید', blank=True, null=True)
    photo_1 = models.ImageField(upload_to='image', blank=True, null=True, default="#")
    photo_2 = models.ImageField(upload_to='image', blank=True, null=True, default="#")
    photo_3 = models.ImageField(upload_to='image', blank=True, null=True, default="#")
    photo_4 = models.ImageField(upload_to='image', blank=True, null=True, default="#")
    photo_5 = models.ImageField(upload_to='image', blank=True, null=True, default='#')

    # bathroom = models.PositiveIntegerField(default=0, null=False, verbose_name='حمام و دستشویی')
    def __str__(self):
        return str(self.title)

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.all()])

    category_to_str.short_description = 'دسته بندی'

    objects = ArticleManager()

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = 'زمان انتشار'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = ' ملک ها '


class PostImage(models.Model):
    post = models.ForeignKey(Article, default=None, on_delete=models.CASCADE)
    photo = models.FileField(upload_to="image", blank=True, null=True, verbose_name='اضافه کردن عکس های بیشتر ')

    def __str__(self):
        return self.post.title
