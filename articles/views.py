from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import Articles
from forums.models import Post
from django.db.models import Q
import random
import bleach
from bleach.css_sanitizer import CSSSanitizer

class SectionsView(TemplateView):
    template_name = 'sections.html'

class ArticlesListView(ListView):
    model = Articles
    template_name = 'articles.html'
    paginate_by = 10
    context_object_name = "items"

    def get_queryset(self):
        section = self.kwargs.get('section')
        return Articles.objects.filter(section=section)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.kwargs.get('section')
        return context

def readArticle(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    allowed_tags = ['b', 'strong', 'i', 'em', 'br', 'p', 'span', 'a', 'big', 'table', 'tr', 'th', 'td', 'hr', 'tbody','a']
    allowed_attributes = {
        '*': ['style', 'class'],
        'a': ['href', 'title'],
        'table': ['border', 'cellpadding', 'cellspacing'],
    }
    
    # Create CSS sanitizer
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=['border', 'border-collapse', 'padding', 
                              'margin', 'width', 'text-align', 'background-color']
    )

    article.body = bleach.clean(
        article.body, 
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=css_sanitizer
    )
    
    try:
        post = Post.objects.get(body=article.question)  # or slug=article.slug
    except Post.DoesNotExist:
        post = None
    return render(request, 'read.html', {
        'article': article,
        'post': post
    })

def random_articles():
    # Define the sections
    sections = [1,2,3,4,5]
    
    articles_data = []
    
    # Get one random article from each section
    for section in sections:
        article = Articles.objects.filter(section=section).order_by('?').first()
        if article:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'preview': article.body[:100] + '...' if len(article.body) > 100 else article.body,
                'section': article.section
            })
    
    return articles_data

