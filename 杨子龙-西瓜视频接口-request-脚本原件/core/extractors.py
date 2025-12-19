# core/extractors.py
import re

def extract_list_id_by_name(html: str, playlist_name: str) -> str:
    """
    从查询接口返回的 html 中，按播放列表名称提取对应的 list_id
    """
    # 思路：匹配 <div class="playlist-item" id="XXXX"> ... >播放列表名<
    pattern = rf'<div class="playlist-item"\s+id="([^"]+)">[\s\S]*?>\s*{re.escape(playlist_name)}\s*<'
    m = re.search(pattern, html)
    if not m:
        raise AssertionError(f"没有在html里找到播放列表名={playlist_name} 对应的list_id")
    return m.group(1)
