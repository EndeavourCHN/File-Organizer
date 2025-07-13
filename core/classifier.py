import os
import yaml

def load_rules(rules_path):
    with open(rules_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def classify(filename, rules, size_threshold=100*1024*1024, clean_large=True, clean_temp=True):
    ext = os.path.splitext(filename)[1].lower()
    size = os.path.getsize(filename)
    if clean_temp and ext in rules.get('temp_exts', []):
        return '临时文件'
    if clean_large and size >= size_threshold:
        return '超大文件'
    for category, exts in rules.get('categories', {}).items():
        if ext in exts:
            return category
    return '其他'
