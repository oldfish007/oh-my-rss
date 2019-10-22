from web.models import *
import feedparser
from feed.utils import current_ts, mark_crawled_url, is_crawled_url
import logging
import django
import requests
from io import BytesIO
# import pysnooper

logger = logging.getLogger(__name__)


# @pysnooper.snoop()
def update_all_user_feed():
    """
    更新所有 site
    """
    logger.info('开始运行定时更新RSS任务')

    feeds = Site.objects.filter(status='active', creator='user').order_by('-star')
    for site in feeds:
        try:
            resp = requests.get(site.rss, timeout=30, verify=False)
        except:
            if site.star >= 9:
                logger.warning(f"RSS源可能失效了`{site.rss}")
            else:
                logger.info(f"RSS源可能失效了`{site.rss}")
            continue

        content = BytesIO(resp.content)
        feed_obj = feedparser.parse(content)

        for entry in feed_obj.entries[:10]:
            try:
                title = entry.title
                link = entry.link
            except AttributeError:
                logger.warning(f'必要属性获取失败：`{site.rss}')
                continue

            if is_crawled_url(link):
                continue

            try:
                author = entry['author'][:11]
            except:
                author = None

            try:
                value = entry.content[0].value
            except:
                value = entry.get('description') or entry.link

            try:
                article = Article(site=site, title=title, author=author, src_url=link, uindex=current_ts(),
                                  content=value)
                article.save()
                mark_crawled_url(link)
            except django.db.utils.IntegrityError:
                logger.info(f'数据重复插入：`{title}`{link}')
            except:
                logger.warning(f'数据插入异常：`{title}`{link}')
    logger.info('定时更新RSS任务运行结束')
