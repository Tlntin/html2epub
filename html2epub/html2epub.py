import os
import shutil
from html2epub.htmlcl import get_img
import html2epub.zipFile as zipFile
from argparse import ArgumentParser
from typing import List, Optional


def cmp(a):
    return int(a.split('-', 1)[0])


class Html2epub:
    def __init__(self, Path, Topath, book_name, content):

        self.path = self.Path2Std(Path)
        self.toPath = self.Path2Std(Topath)
        self.book_name = book_name
        self.content = content

    def start(self):
        # if os.path.exists('temp'):
        #     shutil.rmtree('temp')
        # shutil.copytree('resource', 'temp')
        if not os.path.exists("temp"):
            shutil.copytree('resource', 'temp')
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

        all_file = os.listdir(self.path)


        # all_file = sorted(all_file , key=cmp, reverse=True)

        for _id, html_name in enumerate(all_file, start=1):

            print("process ", html_name, f"{_id}/{len(all_file)}")
            if not html_name.endswith('.html'):
                continue
            name = html_name
            FilePath = self.path + name

            title = name.replace('.html', '')
            toc = toc + navPoint_tmplate.format(id=_id, playOrder=_id, text=title, src=title) + '\n'
            item = item + item_template.format(title=title, id=_id) + '\n'
            item_ref = item_ref + item_ref_template.format(id=_id) + '\n'

            html_file = open(FilePath, 'r', encoding='utf-8')
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

        zipFile.zip_dir(r'temp', self.toPath + self.book_name + '.epub')
        shutil.rmtree('temp')
        print('\nprocess finished')

    def Path2Std(self, Path):

        Path = Path.replace('\\', '/')

        if Path.endswith('/'):
            pass
        else:
            Path += '/'
        return Path


def test(argv: Optional[List[str]] = None):
    parser = ArgumentParser(description='convert html to epub')
    parser.add_argument(
        "--input_dir", type=str,
        help="where you you html in ? give me a dir path"
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
    if args.input_dir is None:
        print(
            "you need to provide dir of html by --input_dir, ",
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
        args.input_dir, args.output_dir, args.title, args.description)
    convter.start()
