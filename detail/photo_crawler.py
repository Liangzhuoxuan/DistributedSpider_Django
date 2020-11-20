import os
from multiprocessing.dummy import Pool
from urllib.request import urlretrieve

class PhotoCrawler:
    # 爬取函数
    def get_photo(self, url):
        part_of_path = r'.\static\img'
        path = os.path.join(part_of_path, url[-16:])
        try:
            # TODO 将这个项目文件放在D盘权限会更高
            urlretrieve(url, path)
        except:
            pass

    # 多线程爬取图片
    def more_processing(self, url_list):
        # 8个线程爬取
        pool = Pool(8)
        results = pool.map(self.get_photo, url_list)
        pool.close()
        pool.join()
