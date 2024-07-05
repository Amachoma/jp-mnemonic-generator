def to_character_markup(character_tags, parent_tag="word"):
    jp_markup = ""
    for tag in character_tags:
        is_plain_string = isinstance(tag, str)
        if is_plain_string:
            jp_markup += tag
            continue

        symbol_markup = ''.join([t for t in tag.contents if isinstance(t, str)])
        furigana_tag = tag.find("rt")

        if furigana_tag:
            furigana = furigana_tag.text
            symbol_markup = f'<kanji furigana="{furigana}">{symbol_markup}</kanji>'

        jp_markup += symbol_markup
    jp_markup = f'<{parent_tag}>{jp_markup}</{parent_tag}>'
    return jp_markup
