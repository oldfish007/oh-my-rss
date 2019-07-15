from django.db import models


class Site(models.Model):
    """
    内容站点定义
    """
    name = models.CharField('对应 scrapy 的 name 代号（不对外显示）', max_length=100, unique=True, db_index=True)
    author = models.CharField('来源站点的作者名', max_length=100)
    cname = models.CharField('来源站点的名称', max_length=100)
    link = models.CharField('来源站点的主页', max_length=200)
    favicon = models.CharField('来源站点的图标，单独制作', max_length=100, default='')
    brief = models.CharField('简介', max_length=200)
    star = models.IntegerField('评级，10，20，30', default=20)
    freq = models.CharField('更新频率', choices=(
        ('日更', '每天更新'),
        ('周更', '每周更新'),
        ('月更', '每月更新'),
    ), max_length=20)
    status = models.CharField('状态，默认 active 激活，close 关闭', max_length=20, choices=(
        ('active', '激活'),
        ('close', '关闭，下线'),
    ), default='active')
    copyright = models.IntegerField('版权', choices=(
        (0, '未知'),
        (10, '不可转载'),
        (20, '仅可转载摘要'),
        (30, '可以全文转载'),
    ), default=0, null=True)

    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    mtime = models.DateTimeField('更新时间', auto_now=True)
    remark = models.TextField('备注', default='', null=True)


class Article(models.Model):
    """
    文章表
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=200, unique=True)
    uindex = models.IntegerField('一个时间戳表示的唯一地址', unique=True, db_index=True)
    content = models.TextField('内容')
    src_url = models.CharField('原始链接', max_length=500)
    status = models.CharField('状态', max_length=20, choices=(
        ('active', '激活'),
        ('close', '关闭，下线'),
    ), default='active')
    readtime = models.IntegerField('预计阅读时间，分钟', default=5)

    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    mtime = models.DateTimeField('更新时间', auto_now=True)
    remark = models.TextField('备注', default='')
