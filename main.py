import requests
import urllib
from bs4 import BeautifulSoup
import re


def parse_search_url(ruleSearchUrl, searchKey):
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


def attach_content(soup, rule):
    rules = rule.split("@")
    if not isinstance(soup, list) and not isinstance(soup, tuple):
        soup = [soup]
    for r in rules:
        r = r.split(".")
        result = []
        for s in soup:
            if len(r) == 1:
                if r[0] == "text":
                    content = s.text
                else:
                    content = s.attrs[r[0]]
                result.append(content)
            elif len(r) == 2 or len(r) == 3:
                if r[0] == "class":
                    content = s.select(f".{r[1]}")
                elif r[0] == "id":
                    content = s.select(f"#{r[1]}")
                elif r[0] == "tag":
                    content = s.select(r[1])
                if len(r) == 3:
                    content = content[int(r[2])]
                    result.append(content)
                else:
                    result += list(content)
            else:
                raise ValueError("The rule is not conform to the regulation.")
        soup = result
    return soup


ruleSearchUrl = "https://www.xbiquge.cc/modules/article/search.php?searchkey=searchKey|char=gbk"
ruleSearchUrl, post_args = parse_search_url(ruleSearchUrl, "我欲")

if post_args is not None:
    searchResult = requests.post(ruleSearchUrl, post_args)
else:
    searchResult = requests.get(ruleSearchUrl)
soup = BeautifulSoup(searchResult.text, "lxml")
print(attach_content(soup, "class.s2@tag.a@text"))
