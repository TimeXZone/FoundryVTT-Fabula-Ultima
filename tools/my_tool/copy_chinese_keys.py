import json
import os
import re

def is_chinese(text):
    # 判断字符串是否包含中文
    return bool(re.search(r'[\u4e00-\u9fff]', str(text)))

def merge_chinese_keys(old_dict, new_dict):
    # 递归合并
    for key, value in old_dict.items():
        if key in new_dict:
            if isinstance(value, dict) and isinstance(new_dict[key], dict):
                merge_chinese_keys(value, new_dict[key])
            elif is_chinese(value):
                new_dict[key] = value

def main():
    old_path = os.path.join('old_version', 'cn.json')
    new_path = os.path.join('new_version', 'cn.json')
    final_path = os.path.join('final_version', 'cn.json')

    with open(old_path, 'r', encoding='utf-8') as f:
        old_json = json.load(f)
    with open(new_path, 'r', encoding='utf-8') as f:
        new_json = json.load(f)

    merge_chinese_keys(old_json, new_json)

    os.makedirs(os.path.dirname(final_path), exist_ok=True)
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(new_json, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()