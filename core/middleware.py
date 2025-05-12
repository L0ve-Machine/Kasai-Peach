# core/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_PATHS = [
    '/password/',              # パスワード入力ページ
    reverse('admin:index'),    # 管理画面
    '/static/',                # 静的ファイル
    '/i18n/',                  # 言語切替
    '/accounts/',              # 認証まわり
]

class SitePasswordMiddleware:
    """
    サイト全体をパスワード保護。セッションに 'passed_site_password' があればOK、
    なければ /password/ にリダイレクト。
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # 除外パスはそのまま通す
        if any(path.startswith(p) for p in EXEMPT_PATHS):
            return self.get_response(request)

        # すでに通過済みならOK
        if request.session.get('passed_site_password'):
            return self.get_response(request)

        # それ以外はパスワード入力ページへ
        return redirect('site_password')
