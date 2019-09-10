import urllib
import urllib.parse
import urllib.request
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_published_signal(sender, **kwargs):
    """Sending signal when an article is published."""
    logger.debug('メソッドガ ヨバレタヨー')
    instance = kwargs['instance']
    if os.getenv('NETLIFY_HOOKS_URL') is None:
        url = ''
    else:
        url = os.getenv('NETLIFY_HOOKS_URL').__str__()
    logger.debug('URL ハ %s ダヨー' % url)
    values = {
        'trigger_branch': 'published',
        'trigger_title': '%s was published.' % instance.title
    }
    headers = {
        'Content-Type': 'application/json',
    }
    data = urllib.parse.urlencode(values).encode()
    logger.debug('データ デキタヨー')
    req = urllib.request.Request(url, data, headers)
    logger.debug('リクエスト ジュンビ デキタヨー')
    res = urllib.request.urlopen(req).read().decode('utf-8')
    logger.debug('リクエスト ケッカ ハ %s ダヨー' % res)


def send_unpublished_signal(sender, **kwargs):
    """Sending signal when an article is unpublished."""
    logger.debug('メソッドガ ヨバレタヨー')
    instance = kwargs['instance']
    if os.getenv('NETLIFY_HOOKS_URL') is None:
        url = ''
    else:
        url = os.getenv('NETLIFY_HOOKS_URL').__str__()
    logger.debug('URL ハ %s ダヨー' % url)
    values = {
        'trigger_branch': 'published',
        'trigger_title': '%s was published.' % instance.title
    }
    headers = {
        'Content-Type': 'application/json',
    }
    data = urllib.parse.urlencode(values).encode()
    logger.debug('データ デキタヨー')
    req = urllib.request.Request(url, data, headers)
    logger.debug('リクエスト ジュンビ デキタヨー')
    res = urllib.request.urlopen(req).read().decode('utf-8')
    logger.debug('リクエスト ケッカ ハ %s ダヨー' % res)
