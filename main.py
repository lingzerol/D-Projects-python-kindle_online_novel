import json
from shelf.mangashelf import MangaShelf

with open("sources.json", "r", encoding="utf-8") as fin:
    book_settings = json.load(fin)

bs = MangaShelf(book_settings)
print(bs.get_chapter_list("https://www.xbiquge.cc/book/52040/", 0))
