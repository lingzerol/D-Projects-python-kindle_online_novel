from .bookshelf import BookShelf

from selenium import webdriver


class MangaShelf(BookShelf):

    def __init__(self, book_settings, logger=None):
        super(MangaShelf, self).__init__(book_settings, logger)
        chrome_options = webdriver.ChromeOptions()  # 设置无头
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(
            "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe", options=chrome_options)

    def get_html(self, url, post_args=None):
        if post_args is not None:
            self.browser.post(url, post_args)
        else:
            self.browser.get(url)
        self.browser.implicitly_wait(5)
        result = self.browser.page_source
        with open("html.txt", "w") as fout:
            fout.write(result)
        return result
