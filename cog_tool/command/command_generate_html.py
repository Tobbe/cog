import argparse
import logging
import os

import cog_tool.data_manipulation as dm
import cog_tool.html as html

def get_command():
    return 'html'

def get_help():
    return 'Export as HTML.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs='*', default='.',
                        help='The files to export. If directory will recursivly add all files. Default: "%(default)s"')
    parser.add_argument('--output', default='html',
                        help='Generate files to this directory. Will be created if needed. Default "%(default)s"')
    return parser

def execute(state, args):
    files = state.expand_paths(args.file)
    data_seq = [state.get_by_path(file)
                for file in files]

    _setup_paths(args)

    _write_html(args.output,
                'index.html',
                _generate_index(data_seq))

    _write_html(args.output,
                'tree.html',
                _generate_tree(state))

    for data in data_seq:
        logging.info('Generating page for "%s"',
                     dm.get(data, 'NAME', '?'))
        html = _generate_html(state, data)
        _write_item(args.output, data, html)

def _setup_paths(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)

def _write_html(root_path, path, html):
    full_path = os.path.join(root_path, path)

    with open(full_path, 'w') as f:
        f.write(str(html))

def _add_link(data, tag):
    id = dm.get(data, 'ID')
    name = dm.get(data, 'NAME', id)
    link = '%s.html' % (id,)
    tag.a(name, href=link)

#--------------------------------------------------
# index

def _generate_index(data_seq):
    logging.info('Generating index page')
    root = html.HTML('html')
    body = root.body()
    body.h1('Item listing')

    tbl = body.table()
    header = tbl.tr()
    header.th('item')

    for data in data_seq:
        name = dm.get(data, 'NAME', dm.get(data, 'ID'))

        tr = tbl.tr()
        _add_link(data, tr.td())

    return root

#--------------------------------------------------
# tree

def _generate_tree(state):
    logging.info('Generating tree page')
    root = html.HTML('html')
    body = root.body()
    body.h1('Tree view (parent)')

    for data in _find_roots(state):
        _generate_tree_data(body.div(), state, data)

    return root

def _generate_tree_data(tag, state, data, type='PARENT',
                        indent=0, max_indent=10):
    tr = tag.table().tr()

    tr.td(dm.get(data, 'NAME'))
    tr.td(dm.get(data, 'ID'), style='color: #aaaaaa;')

    for child in _find_children(state, data):
        _generate_tree_data(tag.div(style='margin-left: 50px'), state, child,
                            type=type, indent=indent + 1, max_indent=max_indent)

def _find_children(state, data, type='PARENT'):
    id = dm.get(data, 'ID')
    result = []

    for child in state.get_all():
        links = child.get(type, [])
        for link in links:
            if link.strip():
                part = link.split()[0]
                if part == id:
                    result.append(child)

    return result

def _find_roots(state, type='PARENT'):
    result = []

    for data in state.get_all():
        if not dm.get(data, type):
            logging.debug('Found root item: %s (%s)',
                          dm.get(data, 'NAME'),
                          dm.get(data, 'ID'))
            result.append(data)

    return result

#--------------------------------------------------
# item html

def _write_item(root_path, data, html):
    id = dm.get(data, 'ID') or dm.get(data, 'NAME')
    path = os.path.join(root_path, '%s.html' % (id,))
    with open(path, 'w') as f:
        f.write(str(html))

def _generate_html(state, data):
    root = html.HTML('html')
    _add_head(data, root)

    body = root.body()
    body.p().a('main', href='index.html')

    _add_core(data, body)
    _add_all_links(state, data, body)

    return root

def _add_head(data, html):
    title = dm.get(data, 'NAME', '?')
    html.head().title(title)
    html.h1(title)

def _add_core(data, tag):
    tbl = tag.table()

    for key in ['NAME', 'ID', 'IMPORTANCE']:
        name = key.lower()
        tr = tbl.tr()
        tr.th(name)
        tr.td(dm.get(data, key, '?'))

def _add_all_links(state, data, tag):
    tbl = tag.table()

    tr = tbl.tr()
    tr.th('type')
    tr.th('direction')
    tr.th('item')

    for link_type in ['PARENT', 'PREREQ', 'LINK']:
        for id in dm.get_links(data, link_type):
            link_data = state.get(id)
            tr = tbl.tr()
            tr.td(link_type.lower())
            tr.td('>>>')
            _add_link(link_data, tr.td())
        for child in state.children(dm.get(data, 'ID'), type=link_type):
            tr = tbl.tr()
            tr.td(link_type.lower())
            tr.td('<<<')
            _add_link(child, tr.td())
