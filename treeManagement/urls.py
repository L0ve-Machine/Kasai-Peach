from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django 管理サイト (必要なら)
    path("admin/", admin.site.urls),

    # 言語切替
    path("i18n/", include("django.conf.urls.i18n")),   # ★プロジェクトレベルで OK

    # 認証 (ログイン /accounts/login/ …)
    path("accounts/", include("django.contrib.auth.urls")),

    # アプリルーティング
    path("", include("core.urls")),                    # ★トップページは core.home
]
