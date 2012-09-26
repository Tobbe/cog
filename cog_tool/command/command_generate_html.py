import argparse
import os

import cog_tool.common as common
import cog_tool.html as html

def get_command():
    return 'html'

def get_help():
    return 'Export as HTML.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('files', nargs='*', default='.',
                        help='The files to export. If directory will recursivly add all files. Default: "%(default)s"')
    parser.add_argument('--output', default='html',
                        help='Generate files to this directory. Will be created if needed. Default "%(default)s"')
    return parser

def execute(args):
    files = common.filter_existing(common.filter_items(common.expand_dirs(args.files)))
    data_seq = [common.load(file)
                for file in files]

    _setup_paths(args)

    _write_html(args.output,
                'index.html',
                _generate_index(data_seq))

    for data in data_seq:
        html = _generate_html(data)
        _write_item(args.output, data, html)

def _setup_paths(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)

def _write_html(root_path, path, html):
    full_path = os.path.join(root_path, path)

    with open(full_path, 'w') as f:
        f.write(str(html))

def _add_link(data, tag):
    id = common.get_value(data, 'ID')
    name = common.get_value(data, 'NAME', id)
    link = '%s.html' % (id,)
    tag.a(name, href=link)

#--------------------------------------------------
# index

def _generate_index(data_seq):
    root = html.HTML('html')
    body = root.body()
    body.h1('Item listing')

    tbl = body.table()
    header = tbl.tr()
    header.th('item')

    for data in data_seq:
        name = common.get_value(data, 'NAME', common.get_value(data, 'ID'))

        tr = tbl.tr()
        _add_link(data, tr.td())

    return root

#--------------------------------------------------
# item html

def _write_item(root_path, data, html):
    id = common.get_value(data, 'ID') or common.get_value(data, 'NAME')
    path = os.path.join(root_path, '%s.html' % (id,))
    with open(path, 'w') as f:
        f.write(str(html))

def _generate_html(data):
    root = html.HTML('html')
    _add_head(data, root)

    body = root.body()
    _add_core(data, body)

    return root

def _add_head(data, html):
    title = common.get_value(data, 'NAME', '?')
    html.head().title(title)
    html.h1(title)

def _add_core(data, tag):
    tbl = tag.table()

    for key in ['NAME', 'ID', 'IMPORTANCE']:
        name = key.lower()
        tr = tbl.tr()
        tr.th(name)
        tr.td(common.get_value(data, key, '?'))
