#!/usr/bin/env python
import os
import django

# ── Django 設定を読み込む ─────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeManagement.settings")
django.setup()

# ── モデルのインポート ───────────────────────────────
from core.models import Variety, Field

# ── 1) ぶどう品種の登録 ─────────────────────────────
grape_varieties = [
    {"name": "シャインマスカット",  "harvest_start": "8月下旬", "qr_prefix": "GSM"},
    {"name": "藤稔",             "harvest_start": "8月中旬", "qr_prefix": "GFM"},
    {"name": "クイーンニーナ",     "harvest_start": "8月中旬", "qr_prefix": "GQN"},
    {"name": "マイハート",         "harvest_start": "8月下旬", "qr_prefix": "GMH"},
    {"name": "甲斐キング",        "harvest_start": "8月中旬", "qr_prefix": "GKK"},
    {"name": "サンシャインレッド", "harvest_start": "8月中旬", "qr_prefix": "GSR"},
]

for v in grape_varieties:
    obj, created = Variety.objects.get_or_create(
        name=v["name"],
        defaults={
            "harvest_start": v["harvest_start"],
            "qr_prefix": v["qr_prefix"]
        }
    )
    print(f"{'作成' if created else '既存'}: 品種 {obj.name}")

# ── 2) ぶどう畑の登録 ───────────────────────────────
grape_fields = [
    {"name":"山・ちどりこ",   "address":"山梨市南1602番地", "area":403,  "variety":"シャインマスカット", "tree_count":7},
    {"name":"山・ちどりこ",   "address":"山梨市南1603番地", "area":341,  "variety":"シャインマスカット", "tree_count":6},
    {"name":"山・ちどりこ",   "address":"山梨市南1604番地", "area":423,  "variety":"シャインマスカット", "tree_count":7},
    {"name":"山・ちどりこ",   "address":"山梨市南1605番地", "area":274,  "variety":"シャインマスカット", "tree_count":3},
    {"name":"山・ちどりこ",   "address":"山梨市南1599番地", "area":480,  "variety":"今から棚立てる",       "tree_count":0},
    {"name":"山・ちどりこ",   "address":"山梨市南1600番地", "area":634,  "variety":"今から棚立てる",       "tree_count":0},
    {"name":"山・ちどりこ",   "address":"山梨市南1601番地", "area":810,  "variety":"今から棚立てる",       "tree_count":0},
    {"name":"古屋さん、川",   "address":"山梨市下栗原511",   "area":1041, "variety":"クイーンニーナ",      "tree_count":0},
    {"name":"シャイン大畑",   "address":"山梨市中村272-1番地", "area":410,  "variety":"シャインマスカット", "tree_count":7},
    {"name":"シャイン大畑",   "address":"山梨市中村273-1番地", "area":683,  "variety":"シャインマスカット", "tree_count":12},
    {"name":"シャイン大畑",   "address":"山梨市中村281番地",   "area":666,  "variety":"シャインマスカット", "tree_count":12},
    {"name":"シャイン大畑",   "address":"山梨市中村279番地",   "area":668,  "variety":"シャインマスカット", "tree_count":12},
    {"name":"共撰所パイプ畑", "address":"山梨市下栗原258-1番地","area":924,  "variety":"シャインマスカット", "tree_count":20},
    {"name":"共撰所杭畑",     "address":"山梨市下栗原21-1番地", "area":1090, "variety":"シャインマスカット", "tree_count":20},
    {"name":"共撰所小屋畑",   "address":"山梨市下栗原528-1番地","area":1982, "variety":"今から棚立てる",       "tree_count":0},
]

created = 0
for f in grape_fields:
    # 品種取得 or 新規作成
    var, _ = Variety.objects.get_or_create(
        name=f["variety"],
        defaults={"harvest_start": "", "qr_prefix": ""}
    )

    Field.objects.create(
        name          = f["name"],
        address       = f["address"],
        area          = f["area"],
        variety       = var,
        tree_count    = f["tree_count"],
        qr_suggestion = ""
    )
    created += 1

print(f"✅ ぶどう畑を {created} 件登録しました。")