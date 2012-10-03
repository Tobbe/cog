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
    parser.add_argument('--output', default='html',
                        help='Generate files to this directory. Will be created if needed. Default "%(default)s"')
    return parser

def execute(state, args):
    _setup_paths(args)

    _write_html(os.path.join(args.output, 'list.html'),
                _generate_item_list(state))

    _write_html(os.path.join(args.output, 'tree.html'),
                _generate_tree(state))

    for data in state.get_all():
        _write_html(os.path.join(args.output, dm.get(data, 'ID') + '.html'),
                    _generate_item_page(state, data))

def _setup_paths(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)

#--------------------------------------------------
# common

def _write_html(path, html):
    with open(path, 'w') as f:
        f.write(str(html))

def _make_page_base(title='?'):
    root = html.HTML('html')
    root.head().title('cog - %s' % (title,))

    body = root.body(style='background: #ccccee;')
    body.h1(title)

    tr = body.table().tr()
    tr.td().a('Item list', href='list.html')
    tr.td().a('Tree', href='tree.html')
    body.hr()

    return (root, body)

def _add_link(tag, data):
    id = dm.get(data, 'ID')
    name = dm.get(data, 'NAME', id)
    link = '%s.html' % (id,)
    tag.a(name, href=link)

#--------------------------------------------------
# item listing

def _generate_item_list(state):
    logging.info('Generating item list')

    root, tag = _make_page_base('Item list')
    items = sorted(state.get_all(),
                   key=lambda x: dm.get(x, 'NAME'))

    tbl = tag.table()
    tr = tbl.tr()
    tr.th('Name')
    tr.th('Priority')
    tr.th('Remaining')

    for data in items:
        tr = tbl.tr()
        _add_link(tr.td(), data)
        tr.td(dm.get(data, 'PRIORITY', '?'))

        remaining = dm.get_remaining_time(data)
        tr.td(str(remaining if not remaining == -1 else '?'))

    return root

#--------------------------------------------------
# tree

def _generate_tree(state, key='PARENT'):
    logging.info('Generating tree')

    root, tag = _make_page_base('Item tree')
    root_items = [data
                  for data in state.get_all()
                  if dm.null(data, key)]

    for data in root_items:
        _generate_tree_item(state, data, tag, key=key)

    return root

def _generate_tree_item(state, data, tag, key='PARENT'):
    id = dm.get(data, 'ID')

    tbl = tag.table(style='margin-left: 50px;')
    tr = tbl.tr()
    _add_link(tr.td(), data)
    tr.td('%s (%s)' % (str(dm.get_remaining_time(data)),
                       str(dm.get_estimate(data))))

    for child_data in state.children(id):
        _generate_tree_item(state, child_data, tbl.tr().td(colspan='2'), key=key)

#--------------------------------------------------
# item pages

def _generate_item_page(state, data):
    name = dm.get(data, 'NAME', '?')
    logging.debug('Generating "%s"', name)
    root, tag = _make_page_base(name)

    # basics
    tbl = tag.table()
    for key in ['ID', 'NAME', 'PRIORITY']:
        title = key.lower()
        tr = tbl.tr()
        tr.th(title)
        tr.td(dm.get(data, key, '?'))

    # parent
    tbl = tag.table()
    tr = tbl.tr()
    tr.th('Parent')
    tr.th('Children')

    tr = tbl.tr()
    parent_td = tr.td()
    child_td = tr.td()

    for id in dm.get_links(data, 'PARENT'):
        other = state.get(id)
        if other:
            _add_link(parent_td.div(), other)

    for other in state.children(dm.get(data, 'ID')):
        if other:
            _add_link(child_td.div(), other)

    # links
    tag.h2('Interesting items')
    lst = tag.ul()
    for id in dm.get_links(data, 'LINK'):
        other = state.get(id)
        if other:
            _add_link(lst.li(), other)

    # time
    total = 0
    for report in dm.get_time_reports(data):
        total += int(report.get('spent'))

    tag.h2('Time')
    tag.p('Estimated time: ' + str(dm.get_estimate(data)))
    tag.p('Total spent: %d' % (total,))

    tbl = tag.table()
    tr = tbl.tr()
    tr.th('Date')
    tr.th('User')
    tr.th('Spent')
    tr.th('Remaining')

    for report in dm.get_time_reports(data):
        tr = tbl.tr()
        for key in ['time', 'user', 'spent', 'remaining']:
            tr.td(str(report.get(key, '')))

    return root
