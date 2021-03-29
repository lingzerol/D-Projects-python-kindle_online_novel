import requests
import urllib
from bs4 import BeautifulSoup
import re
from . import tools


def parse_search_url(ruleSearchUrl: str, searchKey: str):
    if "|" in ruleSearchUrl:
        regex_string = r"(.*)\|char=(.*)"
        match = re.match(regex_string, ruleSearchUrl)
        ruleSearchUrl = match.group(1)
        encoding = match.group(2)
        if "@" not in ruleSearchUrl:
            searchKey = urllib.parse.quote(searchKey.encode(encoding))
    ruleSearchUrl = re.sub("searchKey", searchKey, ruleSearchUrl)
    if "@" in ruleSearchUrl:
        ruleSearchUrl, post_args = ruleSearchUrl.split("@")
        post_args = post_args.split("&")
        post_args = {a.split(
            "=")[0]: a.split(
            "=")[1] for a in post_args}
        return ruleSearchUrl, post_args
    return ruleSearchUrl, None


def attach_content(soup: BeautifulSoup, rule: str):
    if rule == "":
        return []
    rules = rule.split("@")
    if not isinstance(soup, list) and not isinstance(soup, tuple):
        soup = [soup]
    for r in rules:
        if "#" in r:
            r, text = r.split("#")
        else:
            text = None
        r = r.split(".")
        result = []
        for s in soup:
            if len(r) == 1:
                if r[0] == "text":
                    content = s.text
                elif r[0] in s.attrs:
                    content = s.attrs[r[0]]
                else:
                    raise ValueError(
                        "The rule is not conform to the regulation.")
                if text is not None and content.text != text:
                    continue
                result.append(content)
            elif len(r) == 2 or len(r) == 3:
                if r[0] == "class":
                    content = s.select(f".{r[1]}")
                elif r[0] == "id":
                    content = s.select(f"#{r[1]}")
                elif r[0] == "tag":
                    content = s.select(r[1])
                if len(r) == 3:
                    if r[2].startswith("[") and r[2].endswith("]"):
                        if r[2][1] == ">":
                            content = content[min(
                                len(content), int(r[2][2:-1])):]
                        elif r[2][1] == "<":
                            content = content[:min(
                                len(content), int(r[2][2:-1]))]
                        else:
                            ra = r[2][1:-1].split(":")
                            if len(content) < int(ra[2]):
                                content = content[int(ra[0])]
                            else:
                                content = content[int(ra[1])]
                    else:
                        content = content[int(r[2])]
                    if content is not None and not (text is not None and content.text != text):
                        if isinstance(content, list) or isinstance(content, tuple):
                            result += content
                        else:
                            result.append(content)
                else:
                    for c in content:
                        if text is not None and c.text != text:
                            continue
                        result.append(c)
            else:
                raise ValueError("The rule is not conform to the regulation.")
        soup = result
    return soup


bookSourceGroup = "bookSourceGroup"
bookSourceName = "bookSourceName"
bookSourceUrl = "bookSourceUrl"
enable = "enable"
httpUserAgent = "httpUserAgent"
loginUrl = "loginUrl"
ruleBookAuthor = "ruleBookAuthor"
ruleBookContent = "ruleBookContent"
ruleBookKind = "ruleBookKind"
ruleBookLastChapter = "ruleBookLastChapter"
ruleBookName = "ruleBookName"
ruleBookUrlPattern = "ruleBookUrlPattern"
ruleBookUrlPatternBookKey = "ruleBookUrlPatternBookKey"
ruleChapterList = "ruleChapterList"
ruleChapterName = "ruleChapterName"
ruleChapterUrl = "ruleChapterUrl"
ruleChapterUrlPrefix = "ruleChapterUrlPrefix"
ruleChapterUrlNext = "ruleChapterUrlNext"
ruleChapterUrlNextPrefix = "ruleChapterUrlNextPrefix"
ruleContent = "ruleContent"
ruleContentUrlNext = "ruleContentUrlNext"
ruleContentUrlNextPrefix = "ruleContentUrlNextPrefix"
ruleCoverUrl = "ruleCoverUrl"
ruleFindUrl = "ruleFindUrl"
ruleIntroduce = "ruleIntroduce"
ruleSearchAuthor = "ruleSearchAuthor"
ruleSearchCoverUrl = "ruleSearchCoverUrl"
ruleSearchKind = "ruleSearchKind"
ruleSearchLastChapter = "ruleSearchLastChapter"
ruleSearchList = "ruleSearchList"
ruleSearchName = "ruleSearchName"
ruleSearchNoteUrl = "ruleSearchNoteUrl"
ruleSearchUrl = "ruleSearchUrl"
serialNumber = "serialNumber"
weight = "weight"


class BookShelf:
    def __init__(self, book_settings, logger=None):
        super(BookShelf, self).__init__()
        self.book_settings = book_settings
        if logger is None:
            self.logger = tools.get_logger("BookShelf")
        else:
            self.logger = logger
        self.max_iter = 50

    def get_html(self, url, post_args=None):
        if post_args is not None:
            html = requests.post(url, post_args)
        else:
            html = requests.get(url)
        return html.text

    def get_next_page(self, link, soup, rule_next, rule_next_prefix):
        if rule_next != "":
            next_page = attach_content(
                soup, rule_next)[0]
            if tools.check_url(next_page):
                result = next_page
            elif tools.check_url(self._complete_link(link,
                                                     next_page, rule_next_prefix)):
                result = self._complete_link(link,
                                             next_page, rule_next_prefix)
            return result
        else:
            return ""

    def search(self, name):
        result = {}

        def _insert_book_info(result, source, book_name, author_name,
                              book_url, book_kind, book_cover, book_last_chapter, setting_id):
            if (book_name, author_name) in result:
                result[(book_name, author_name)]["sources"].append(source)
                result[(book_name, author_name)]["urls"].append(book_url)
                result[(book_name, author_name)]["covers"].append(book_cover)
                result[(book_name, author_name)]["kinds"].append(book_kind)
                result[(book_name, author_name)
                       ]["last_chapters"].append(book_last_chapter)
                result[(book_name, author_name)]["settings"].append(setting_id)
            else:
                result[(book_name, author_name)] = {}
                result[(book_name, author_name)]["sources"] = [source]
                result[(book_name, author_name)]["urls"] = [book_url]
                result[(book_name, author_name)]["covers"] = [book_cover]
                result[(book_name, author_name)]["kinds"] = [book_kind]
                result[(book_name, author_name)]["last_chapters"] = [
                    book_last_chapter]
                result[(book_name, author_name)]["settings"] = [setting_id]

        for i, bs in enumerate(self.book_settings):
            try:
                url, post_args = parse_search_url(
                    bs[ruleSearchUrl], name)
                if post_args is not None:
                    post_args[httpUserAgent] = bs[httpUserAgent]
                search_html = self.get_html(url, post_args)
                soup = BeautifulSoup(search_html.text, "lxml")
                book_list = attach_content(soup, bs[ruleSearchList])
                book_name = attach_content(soup, bs[ruleBookName])
                if len(book_name) > 0:
                    book_name, author_name, book_kind, book_cover, book_last_chapter = self.get_book_info(
                        search_html.url, i)
                    _insert_book_info(
                        result, bs[bookSourceName], book_name, author_name,
                        search_html.url, book_kind, book_cover, book_last_chapter, i)
                elif len(book_list) > 0:
                    book_names = attach_content(
                        soup, bs[ruleSearchList]+"@"+bs[ruleSearchName])
                    if bs[ruleSearchAuthor] != "":
                        author_names = attach_content(
                            soup, bs[ruleSearchList]+"@"+bs[ruleSearchAuthor])
                    else:
                        author_names = [""]*len(book_names)
                    book_urls = attach_content(
                        soup, bs[ruleSearchList]+"@"+bs[ruleSearchNoteUrl])
                    if bs[ruleSearchKind] != "":
                        book_kinds = attach_content(
                            soup, bs[ruleSearchList]+"@"+bs[ruleSearchKind])
                    else:
                        book_kinds = [""]*len(book_names)
                    if bs[ruleSearchCoverUrl] != "":
                        book_covers = attach_content(
                            soup, bs[ruleSearchList]+"@"+bs[ruleSearchCoverUrl])
                    else:
                        book_covers = [""]*len(book_names)
                    if bs[ruleSearchLastChapter] != "":
                        book_last_chapters = attach_content(
                            soup, bs[ruleSearchList]+"@"+bs[ruleSearchLastChapter])
                    else:
                        book_last_chapters = [""]*len(book_names)
                    for bn, an, bu, bk, bc, blc in zip(book_names, author_names, book_urls, book_kinds, book_covers, book_last_chapters):
                        _insert_book_info(
                            result, bs[bookSourceName], bn, an, bu, bk, bc, i)
            except Exception as err:
                self.logger.error(err)
        return result

    def get_book_info(self, book_link, setting_id):
        setting = self.book_settings[setting_id]
        html = self.get_html(book_link)
        soup = BeautifulSoup(html, "lxml")
        try:
            book_name = attach_content(soup, setting[ruleBookName])[0]
            author_name = attach_content(soup, setting[ruleBookAuthor])[0]
            if setting[ruleBookKind] != "":
                book_kind = attach_content(soup, setting[ruleBookKind])[0]
            else:
                book_kind = ""
            if setting[ruleCoverUrl] != "":
                book_cover = attach_content(soup, setting[ruleCoverUrl])[0]
            else:
                book_cover = ""
            if setting[ruleBookLastChapter] != "":
                book_last_chapter = attach_content(
                    soup, setting[ruleBookLastChapter])[0]
            else:
                book_last_chapter = ""
        except Exception as err:
            self.logger.error(err)
        return book_name, author_name, book_kind, book_cover, book_last_chapter

    def get_content(self, chapter_link, setting_id):
        setting = self.book_settings[setting_id]
        chapter_link = chapter_link
        result = []
        try:
            for _ in range(self.max_iter):
                html = self.get_html(chapter_link)
                soup = BeautifulSoup(html, "lxml")
                content = attach_content(soup, setting[ruleContent])
                result += content
                chapter_link = self.get_next_page(
                    chapter_link, soup, setting[ruleContentUrlNext],  setting[ruleContentUrlNextPrefix])
                if chapter_link == "":
                    break
        except Exception as err:
            self.logger.error(err)
        return result

    def get_chapter_list(self, book_link, setting_id):
        setting = self.book_settings[setting_id]
        chapter_link = book_link
        result = []
        try:
            for _ in range(self.max_iter):
                html = self.get_html(chapter_link)
                soup = BeautifulSoup(html, "lxml")
                chapter_names = attach_content(
                    soup, setting[ruleChapterList]+"@"+setting[ruleChapterName])
                chapter_urls = attach_content(
                    soup, setting[ruleChapterList]+"@"+setting[ruleChapterUrl])
                for name, url in zip(chapter_names, chapter_urls):
                    if tools.check_url(url):
                        result.append([name, url])
                    elif tools.check_url(self._complete_link(book_link,
                                                             url, setting[ruleChapterUrlPrefix])):
                        result.append([name, self._complete_link(book_link,
                                                                 url, setting[ruleChapterUrlPrefix])])
                    else:
                        continue
                chapter_link = self.get_next_page(
                    chapter_link, soup, setting[ruleChapterUrlNext],  setting[ruleChapterUrlNextPrefix])
                if chapter_link == "":
                    break
        except Exception as err:
            self.logger.error(err)
        return result

    def get_setting(self, setting_id):
        return self.book_settings[setting_id]

    def _complete_link(self, book_link, link, prefix):
        links = book_link.split("/")
        if prefix != "":
            links = links[:int(prefix)]
        links.append(link)
        result = "/".join(links)
        return result
