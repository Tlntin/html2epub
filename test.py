from argparse import ArgumentParser
from html2epub.html2epub import Html2epub


if __name__ == '__main__':
    parser = ArgumentParser(description='convert html to epub')
    parser.add_argument(
        "--input_dir", type=str,
        help="where you save you html? give me a path"
    )
    parser.add_argument(
        "--output_dir", type=str,
        help="where you want to save?"

    )
    parser.add_argument(
        "--title", type=str, help="the title of book",
        default=None, required=False)
    parser.add_argument("--description", type=str, default=None, required=False)
    args = parser.parse_args()
    convter = Html2epub(
        args.input_dir, args.output_dir, args.title, args.description)
    convter.start()