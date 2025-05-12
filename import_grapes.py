#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeManagement.settings")
django.setup()

from core.models import Variety, Field

# 1) ぶどう品種の登録
grape_varieties = [
    {"name": "シャインマスカット",  "harvest_start": "8月下旬", "qr_prefix": "GSM"},
    {"name": "藤稔",             "harvest_start": "8月中旬", "qr_prefix": "GFM"},
    {"name": "クイーンニーナ",     "harvest_start": "8月中旬", "qr_prefix": "GQN"},
    {"name": "マイハート",         "harvest_start": "8月下旬", "qr_prefix": "GMH"},
    {"name": "甲斐キング",        "harvest_start": "8月中旬", "qr_prefix": "GKK"},
    {"name": "サンシャインレッド", "harvest_start": "8月中旬", "qr_prefix": "GSR"},
]

for v in grape_varieties:
    obj, created = Variety.objects.update_or_create(
        name=v["name"],
        defaults={
            "harvest_start": v["harvest_start"],
            "qr_prefix": v["qr_prefix"],
            "fruit_type": "grape",      # ← ここを追加
        }
    )
    print(f"{'作成' if created else '更新'}: 品種 {obj.name} (fruit_type={obj.fruit_type})")

# 2) ぶどう畑の登録
grape_fields = [
    {"name":"山・ちどりこ",   "address":"山梨市南1602番地", "area":403,  "variety":"シャインマスカット", "tree_count":7},
    # 省略…
]

created = 0
for f in grape_fields:
    var = Variety.objects.get(name=f["variety"])  # 上で作った grape 品種を取得
    Field.objects.create(
        name          = f["name"],
        address       = f["address"],
        area          = f["area"],
        variety       = var,
        tree_count    = f["tree_count"],
        qr_suggestion = "",
    )
    created += 1

print(f"✅ ぶどう畑を {created} 件登録しました。")
