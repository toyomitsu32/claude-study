#!/usr/bin/env python3
"""
公開版ビルド用スクリプト
- data-libecity 属性を持つ要素を丸ごと削除
- data-public-only 属性を持つ要素の display:none を除去して表示
- HTMLコメント中の「リベシティ」も除去
"""

import re
import sys
import os
from html.parser import HTMLParser


class LibecityStripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.output = []
        self.skip_depth = 0  # data-libecity 要素のネスト深さ
        self.skip_tag = None  # スキップ中のタグ名
        self.skip_tag_depth = 0  # 同名タグのネスト数

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        if self.skip_depth > 0:
            if tag == self.skip_tag:
                self.skip_tag_depth += 1
            return

        if 'data-libecity' in attr_dict:
            self.skip_depth = 1
            self.skip_tag = tag
            self.skip_tag_depth = 1
            return

        if 'data-public-only' in attr_dict:
            # display:none を除去して表示
            new_attrs = []
            for name, value in attrs:
                if name == 'data-public-only':
                    continue
                if name == 'style' and value:
                    value = re.sub(r';?\s*display\s*:\s*none\s*;?', '', value).strip()
                    value = value.rstrip(';')
                    if not value:
                        continue
                new_attrs.append((name, value))
            self.output.append(self._build_tag(tag, new_attrs))
            return

        self.output.append(self._build_tag(tag, attrs))

    def handle_endtag(self, tag):
        if self.skip_depth > 0:
            if tag == self.skip_tag:
                self.skip_tag_depth -= 1
                if self.skip_tag_depth == 0:
                    self.skip_depth = 0
                    self.skip_tag = None
            return

        self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        self.output.append(data)

    def handle_comment(self, data):
        if self.skip_depth > 0:
            return
        # リベシティ版コメントは除去
        if 'リベシティ版' in data:
            return
        self.output.append(f'<!--{data}-->')

    def handle_entityref(self, name):
        if self.skip_depth > 0:
            return
        self.output.append(f'&{name};')

    def handle_charref(self, name):
        if self.skip_depth > 0:
            return
        self.output.append(f'&#{name};')

    def handle_decl(self, decl):
        self.output.append(f'<!{decl}>')

    def handle_pi(self, data):
        if self.skip_depth > 0:
            return
        self.output.append(f'<?{data}>')

    def _build_tag(self, tag, attrs):
        parts = [tag]
        for name, value in attrs:
            if value is None:
                parts.append(name)
            else:
                parts.append(f'{name}="{value}"')
        return '<' + ' '.join(parts) + '>'

    def get_result(self):
        result = ''.join(self.output)
        # 連続する空行を整理
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result


def strip_libecity(html: str) -> str:
    stripper = LibecityStripper()
    stripper.feed(html)
    return stripper.get_result()


def process_file(filepath: str) -> None:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    result = strip_libecity(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

    # 残留チェック
    remaining = len(re.findall(r'libecity|リベシティ|ノウハウ図書館', result))
    print(f'Processed: {filepath} (remaining libecity refs: {remaining})')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            process_file(path)
    else:
        dist_path = os.path.join('dist', 'public', 'index-content.html')
        if os.path.exists(dist_path):
            process_file(dist_path)
        else:
            print(f'File not found: {dist_path}')
            sys.exit(1)
