from revproxy.views import ProxyView

from .app_helpers import get_articles
from .tasks import add_user_to_mailing_list_task


class DevelopmentNextjsProxyView(ProxyView):
    upstream = 'http://localhost:3000'
