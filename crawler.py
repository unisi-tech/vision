from icrawler.builtin import GoogleImageCrawler
import os, time, config, unigui, common

def get_pictures(theme):
    """returns folder name with pictures if ok"""
    folder = f'{config.upload_dir}{unigui.divpath}{theme}-{int(time.time())}' 
    google_crawler = GoogleImageCrawler(storage={'root_dir': folder})
    google_crawler.crawl(keyword=theme, max_num=100)
    if common.exists(folder) and os.listdir(folder):
        return folder