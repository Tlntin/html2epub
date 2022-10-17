import os
import shutil
from html2epub.htmlcl import get_img
import html2epub.zipFile as zipFile
from argparse import ArgumentParser
from typing import List, Optional
import sys
import pkg_resources
import requests
from random import randint


def cmp(a):
    return int(a.split('-', 1)[0])


class Html2epub:
    def __init__(self, url, html_path, input_dir, output_dir, book_name, content):
        self.url = url
        self.html_path = self.path2std(html_path)
        self.input_dir = self.path2std(input_dir)
        self.out_put_dir = self.path2std(output_dir)
        self.now_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.resource_dir = os.path.join(self.now_dir, "resource")
        if not os.path.exists(self.resource_dir):
            temp_dir = pkg_resources.resource_filename(__name__, "")
            self.resource_dir = os.path.join(
                os.path.dirname(temp_dir),
                "share/doc/html2epub/resource"
            )
        if not os.path.exists(self.resource_dir):
            temp_dir = sys.prefix
            self.resource_dir = os.path.join(
                temp_dir,
                "share/doc/html2epub/resource"
            )
        print("resource dir ", self.resource_dir)
        self.book_name = book_name
        self.content = content

    def start(self):
        if not os.path.exists("temp"):
            shutil.copytree(self.resource_dir, 'temp')
        # just to save image
        if not os.path.exists("Images"):
            os.mkdir("Images")
        if not os.path.exists("temp/Text"):
            os.mkdir("temp/Text")
        if not os.path.exists("temp/Images"):
            os.makedirs('temp/Images')

        navPoint_tmplate = '''
        <navPoint id="{id}" playOrder="{playOrder}">
              <navLabel>
                <text>{text}</text>
              </navLabel>
              <content src="Text/{src}.html"/>
        </navPoint>
        '''

        item_template = '''
        <item href="Text/{title}.html" id="{id}" media-type="application/xhtml+xml"/>
        '''

        item_ref_template = '''
        <itemref idref="{id}"/>
        '''

        toc = ''
        item = ''
        item_ref = ''
        opf_file = open(r'temp/content.opf', 'r', encoding='utf-8')
        opf_content = opf_file.read()

        opf_file.close()

        toc_file = open(r'temp/toc.ncx', 'r', encoding='utf-8')
        toc_content = toc_file.read()
        toc_file.close()
        all_file = []
        if self.input_dir is not None:
            all_file.extend(os.listdir(self.input_dir))
        if self.html_path is not None:
            all_file.append(self.html_path)
        if self.input_dir is None:
            self.input_dir = "html"
            if not os.path.exists(self.input_dir):
                os.mkdir(self.input_dir)
        if self.url is not None:
            temp_file = f"{randint(1, 1000)}.html"
            temp_path = os.path.join(self.input_dir, temp_file)
            i_headers = {
                            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                            "Accept": "text/plain"
                        }
            res = requests.get(self.url, headers=i_headers, timeout=10)
            if res.status_code == 200:
                f = open(temp_path, "wb")
                f.write(res.content)
                all_file.append(temp_file)


        # all_file = sorted(all_file , key=cmp, reverse=True)

        for _id, html_name in enumerate(all_file, start=1):

            print("process ", html_name, f"{_id}/{len(all_file)}")
            if not html_name.endswith('.html'):
                continue
            file_path = os.path.join(self.input_dir, html_name)
            title = html_name.replace('.html', '')
            toc = toc + navPoint_tmplate.format(id=_id, playOrder=_id, text=title, src=title) + '\n'
            item = item + item_template.format(title=title, id=_id) + '\n'
            item_ref = item_ref + item_ref_template.format(id=_id) + '\n'

            html_file = open(file_path, 'r', encoding='utf-8')
            html_content = html_file.read()
            html_file.close()

            replaced_html = [html_content]
            Parser = get_img(html=replaced_html, path=r'temp/')

            Parser.feed(html_content)
            
            html_file = open(r'temp/Text/' + title + '.html', 'w', encoding='utf-8')
            html_file.write(replaced_html[0])
            html_file.close()

        toc_file = open(r'temp/toc.ncx', 'w', encoding='utf-8')
        toc_file.write(toc_content.format(toc))
        toc_file.close()

        opf_file = open(r'temp/content.opf', 'w', encoding='utf-8')
        opf_file.write(opf_content.format(title=self.book_name, content1=self.content, content2=self.content, item=item,
                                          item_ref=item_ref))
        opf_file.close()
        epub_path = os.path.join(self.out_put_dir, self.book_name + '.epub')
        zipFile.zip_dir('temp', epub_path)
        shutil.rmtree('temp')
        print(f'\nprocess finished, output_path is {epub_path}')

    @staticmethod
    def path2std(input_path):
        if isinstance(input_path, str):
            input_path = input_path.replace('\\', '/')
        return input_path


def test(argv: Optional[List[str]] = None):
    parser = ArgumentParser(description='convert html to epub')
    parser.add_argument(
        "--url", type=str, default=None, required=False,
       help="when you set the url, we can get it's html content, then convter it to epub!" 
    )
    parser.add_argument(
        "--html_path", type=str, default=None, required=False,
        help="where is you html ? give me a file path"
    )
    parser.add_argument(
        "--input_dir", type=str, default=None, required=False,
        help="where is you html ? give me a dir path"
    )
    parser.add_argument(
        "--output_dir", type=str,
        help="where you want to save the epub file? give me a dir path"

    )
    parser.add_argument(
        "--title", type=str,  help="the title of book",
        default=None)
    parser.add_argument(
        "--description", type=str, default="",required=False,
        help="description of book, it's optional!"
    )
    args = parser.parse_args(argv)
    if args.input_dir is None and args.url is None and args.html_path is None:
        print(
            "you need to provide dir of html by --input_dir or provider url by --url or html path with --html_path ",
            "use --help to see more infomation!"
        )
        return 1
    if isinstance(args.input_dir, str) and not os.path.exists(args.input_dir):
        print(
            "you provider input_dir is not exist, please check it again!",
            "use --help to see more infomation!"
        )
        return 1
    if isinstance(args.input_dir, str) and len(os.listdir(args.input_dir)) == 0:
        print(
            "can't found any html file in input_dir, please check it again!",
            "use --help to see more infomation!"
        )
        return 1
    if args.output_dir is None:
        print(
            "you need to provide output dir of html with --output_dir",
            "use --help to see more infomation!"
        )
        return 1
    if isinstance(args.input_dir, str) and not os.path.exists(args.input_dir):
        print(
            "you provider output_dir is not exist, please check it again!"
            "use --help to see more infomation!"
        )
        return 1
    convter = Html2epub(
        args.url, args.html_path, args.input_dir, args.output_dir, args.title, args.description)
    convter.start()
