from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Site, Article


class SiteFeed(Feed):
    ttl = 7200

    def get_object(self, request, name):
        return Site.objects.get(name=name, status='active', creator__in=('system', 'wemp'))

    def title(self, site):
        return site.cname

    def link(self, site):
        return site.link

    def description(self, site):
        return site.brief

    def feed_url(self, site):
        return reverse('get_feed_entries', kwargs={"name": site.name})

    def author_name(self, site):
        return site.author

    def categories(self, site):
        return site.tag.split('|')

    def items(self, site):
        return Article.objects.filter(site=site, status='active').order_by('-ctime')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.src_url

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.ctime
