#!/usr/bin/env python3
import os, sys
from flup.server.fcgi import WSGIServer

# vendor フォルダをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vendor'))
# プロジェクトルートもパスに追加
sys.path.insert(0, os.path.dirname(__file__))

# Django の settings を指定（プロジェクト名に合わせてください）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeManagement.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# FastCGI でアプリを起動
WSGIServer(application).run()