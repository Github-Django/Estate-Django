from .models import Article, Category, PostImage
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from account.mixin import AuthorAccsesMixin
from .filter import ProductFilter
from django.core.paginator import Paginator
from django.db.models import Min, Max, Q
from urllib.parse import urlencode
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import uri_to_iri

# Create your views here.

def ArticleList(request):
    articles = Article.objects.published().order_by('-publish')[:3]
    specials = Article.objects.published().order_by('-Special2', '-updated')[:3]
    context = {
        "articles": articles,
        'specials': specials
    }

    return render(request, 'blog/home.html', context)


def SpecialListing(request):
    articles = Article.objects.published().order_by('-publish')
    context = {
        "articles": articles,
    }
    return render(request, 'blog/special-listing.html', context)


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        global similar, photos
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=uri_to_iri(slug))
        similar = article.tags.similar_objects()[:3]
        photos = PostImage.objects.filter(post=article)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar'] = similar
        context['photos'] = photos
        return context


class ArticlePreview(AuthorAccsesMixin, DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


def ListProperty(request):
    list_article = Article.objects.published().order_by('-publish')
    # filter price
    min = Article.objects.aggregate(price=Min('unit_price'))
    min_price = int(min['price'])
    max = Article.objects.aggregate(price=Max('unit_price'))
    max_price = int(max['price'])
    filter = ProductFilter(request.GET, queryset=list_article)
    list_article = filter.qs
    # area
    min = Article.objects.aggregate(area=Min('area'))
    min_area = int(min['area'])
    max = Article.objects.aggregate(area=Max('area'))
    max_area = int(max['area'])
    # pagination
    paginator = Paginator(list_article, 15)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    data = request.GET.copy()
    if 'page' in data:
        del data['page']
    # search
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            articles = list_article.filter(
                Q(description__icontains=search) | Q(title__icontains=search) | Q(code__icontains=search))
    context = {
        "articles": articles,
        'filter': filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_area': min_area,
        'max_area': max_area,
        'values': request.GET,
        # 'bedroom_choices': bedroom_choices,
        'data': urlencode(data)

    }
    return render(request, 'blog/simple-listing-fw.html', context)


def GridProperty(request):
    list_article = Article.objects.published().order_by('-publish')

    filter = ProductFilter(request.GET, queryset=list_article)
    list_article = filter.qs
    # pagination
    paginator = Paginator(list_article, 15)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        "articles": articles,
        'filter': filter,

    }
    return render(request, 'blog/grid-listing-fw.html', context)


class CategoryList(ListView):
    paginate_by = 15
    template_name = 'blog/category-listing-fw.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return Article.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 15
    template_name = 'blog/author.html'

    def get_queryset(self):
        global author
        phone = self.kwargs.get('phone')
        author = get_object_or_404(User, phone=phone)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


def notfound(request, exception):
    return render(request, 'blog/404.html')
