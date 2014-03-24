from django import template
from django.db.models.aggregates import Count
from mysite.forum.models import Categories, Subcategories, Messages, Topics

register = template.Library()

@register.inclusion_tag('categories_template/cat.html')
def show_cat():
    cats = Categories.objects.all()
    subcats = Subcategories.objects.all()
    return {'cats': cats,'subcats':subcats}


@register.inclusion_tag('categories_template/news.html')
def show_news():
#    msgs = Messages.objects.order_by('-update_date').values('topic').distinct()[:3]
#    tops_id = set()
#    for msg in msgs:
#        tops_id.add(msg.get('topic'))
    news = Topics.objects.order_by('-update_date')[:3]
#    subcats_id =set()
#    for new in news:
#        subcats_id.add(new.subcategory)
#    subcats = Subcategories.objects.filter(id__in=subcats_id)

    return {'news': news}