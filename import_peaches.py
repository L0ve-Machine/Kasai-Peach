#!/usr/bin/env python
import os
import django

# ── Django設定の読み込み ───────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeManagement.settings")
django.setup()

# ── モデルのインポート ─────────────────────────────
from core.models import Variety

# ── 桃品種データ ──────────────────────────────────
peach_varieties = [
    {"name":"日川",       "harvest_start":"6月中・下旬", "qr_prefix":"PHI0000"},
    {"name":"加納岩",     "harvest_start":"6月下旬",     "qr_prefix":"PKA0000"},
    {"name":"夢香桃",     "harvest_start":"6月下旬",     "qr_prefix":"PYT0000"},
    {"name":"白鳳",       "harvest_start":"7月上旬",     "qr_prefix":"PHA0000"},
    {"name":"夢みずき",   "harvest_start":"7月上旬",     "qr_prefix":"PYM0000"},
    {"name":"浅間",       "harvest_start":"7月中旬",     "qr_prefix":"PAS0000"},
    {"name":"れいほう",   "harvest_start":"7月中旬",     "qr_prefix":"PRE0000"},
    {"name":"なつっこ",   "harvest_start":"7月下旬",     "qr_prefix":"PNA0000"},
    {"name":"紅くにか",   "harvest_start":"7月下旬",     "qr_prefix":"PBK0000"},
    {"name":"川中島",     "harvest_start":"8月上旬",     "qr_prefix":"PKW0000"},
    {"name":"幸茜",       "harvest_start":"8月中旬",     "qr_prefix":"PSA0000"},
    {"name":"さくら",     "harvest_start":"8月中旬",     "qr_prefix":"PSK0000"},
    {"name":"甲斐黄色",   "harvest_start":"8月下旬",     "qr_prefix":"PKK0000"},
    # 他の品種が増える場合はこのリストに追加…
]

# ── 登録／更新処理 ──────────────────────────────────
for v in peach_varieties:
    obj, created = Variety.objects.update_or_create(
        name=v["name"],
        defaults={
            "harvest_start": v["harvest_start"],
            "qr_prefix": v["qr_prefix"],
        }
    )
    action = "作成" if created else "更新"
    print(f"{action}：品種「{obj.name}」 → 収穫開始={obj.harvest_start}, QR接頭辞={obj.qr_prefix}")

print("✅ 桃品種の登録・更新が完了しました。")
