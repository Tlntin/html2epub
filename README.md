## what is?
- conveter html filt to epub file.
- it will download image url when convert.
- it can merge many html to one epub file.
- refer [link](https://gitee.com/alexi126/html2epub.git)

## how to use

- install
```bash
git clone https://github.com/Tlntin/html2epub
cd html2epub
python setup.py install
# or
pip install git+https://github.com/Tlntin/html2epub
```

- use
```bash
# use with cli
html2epub \
    --input_dir=xxxxx \  # or --html_path or --url
    --output_dir=xxxxxxx \ 
    --title="xxxxx" \
    --description="xxxxx"

# use with module
# see test.py
```

