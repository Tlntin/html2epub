from html.parser import HTMLParser
import hashlib
import requests
import shutil
import os


class get_img(HTMLParser):
    def __init__(self, html, path):
        self.html = html
        self.path = path
        self.img_num = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):

        if tag == 'img':
            src_attrs = [attr for attr in attrs if attr[0] == "src"]
            for _, value in src_attrs:
                self.img_num += 1
                print(f"\rdownload {self.img_num} picture", end="")
                hash = hashlib.md5(value.encode('utf-8')).hexdigest().upper()
                new_url = "Images/" + hash + '.png'
                temp_image_path = self.path + new_url
                if os.path.exists(new_url) and os.path.getsize(new_url) > 0:
                    shutil.copyfile(new_url, temp_image_path)
                else:
                    try:
                        i_headers = {
                            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                            "Accept": "text/plain"}

                        res = requests.get(value, headers=i_headers, timeout=10)
                        if res.status_code == 200:
                            f = open(temp_image_path, "wb")
                            f.write(res.content)
                            f.close()
                            shutil.copyfile(temp_image_path, new_url)
                        else:
                            print("Network error!", res)
                            
                    except Exception as e:
                        print("image download failed", e)
                old_str = '"' + value + '"'
                new_str = '"../' + new_url + '"'
                self.html[0] = self.html[0].replace(old_str, new_str)
