from argparse import ArgumentParser
import os
from html2epub.html2epub import Html2epub


if __name__ == '__main__':
    url = "https://www.baidu.com"
    html_path = None
    input_dir = None
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    title = "百度"
    describe = ""
    convter = Html2epub(url, html_path, input_dir, output_dir, title, describe)
    convter.start()