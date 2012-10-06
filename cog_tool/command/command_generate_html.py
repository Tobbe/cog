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
    head = root.head()
    head.title('cog - %s' % (title,))
    head.link(rel='stylesheet', type='text/css', href='cog.css')

    main = root.body().div(klass='main')

    tr = main.table().tr()
    tr.td().raw_text('Cog&nbsp;HTML&nbsp;export')
    tr.td().a('List', href='list.html')
    tr.td().a('Tree', href='tree.html')
    tr.td(width='100%')
    main.hr()

    main.h1(title)

    return (root, main)

def _add_link(tag, data):
    id = dm.get(data, 'ID')
    name = dm.get(data, 'NAME', id)
    link = '%s.html' % (id,)
    tag.a(name, href=link)

def _make_relative_meter(tag, offset, total):
    ratio = (float(offset) / total) * 50
    ratio = min(ratio, 50)
    ratio = max(ratio, -50)

    tbl = tag.table(klass='bar')
    tr = tbl.tr()

    if ratio < 0:
        tr.td(klass='bar_none')
        tr.td(klass='bar_bad', style='width: %.0f%%;' % (-ratio,))
        tr.td(klass='bar_none', style='width: 50%;')
    else:
        tr.td(klass='bar_none', style='width: 50%;')
        tr.td(klass='bar_good', style='width: %.0f%%;' % (max(ratio, 1),))
        tr.td(klass='bar_none')

#--------------------------------------------------
# item listing

def _generate_item_list(state):
    logging.info('Generating item list')

    root, tag = _make_page_base('Item list')
    data_seq = sorted(state.get_all(),
                   key=lambda x: dm.get(x, 'NAME'))

    grouped_data = _group_items(data_seq)

    for key in ['ongoing', 'waiting', 'not-started', 'done']:
        if key in grouped_data:
            tag.h2(key)
            _generate_item_list_part(tag, grouped_data[key])
            tag.br()

    return root

def _group_items(data_seq):
    result = {}

    for data in data_seq:
        status = dm.get_status(data)
        if not status in result:
            result[status] = []
        result[status].append(data)

    return result

def _generate_item_list_part(tag, data_seq):
    tbl = tag.table()
    tr = tbl.tr()
    for name in ['Task', 'Assigned', 'Estimated', 'Left', 'On track-o-meter', 'Projection']:
        tr.th(name)

    for data in data_seq:
        spent = dm.get_time_spent(data)
        remaining = dm.get_remaining_time(data)
        estimate = dm.get_estimate(data)
        time_projection = dm.get_projected_time_diff(data)

        tr = tbl.tr()
        _add_link(tr.td(), data)
        tr.td(dm.get(data, 'ASSIGNED', '-'))
        tr.td(str(estimate))
        tr.td('%d' % (remaining,))
        _make_relative_meter(tr.td(), -time_projection, estimate)
        tr.td('%+d' % (time_projection,))

#--------------------------------------------------
# tree

def _generate_tree(state, key='PARENT'):
    logging.info('Generating tree')

    root, tag = _make_page_base('Item tree')
    root_items = [data
                  for data in state.get_all()
                  if dm.null(data, key)]

    tbl = tag.table(klass='small')
    for status in ['not-started', 'ongoing', 'waiting', 'done']:
        tr = tbl.tr()
        tr.td(klass='status-box status-%s' % (status,))
        tr.td(status)

    for data in root_items:
        _generate_tree_item(state, data, tag, key=key, indent=False)

    return root

def _generate_tree_item(state, data, tag, key='PARENT', indent=True):
    id = dm.get(data, 'ID')

    tbl = tag.table(klass='tree')
    tr = tbl.tr()

    status = dm.get_status(data)
    tr.td(klass='status-box status-%s' % (status,))
    _add_link(tr.td(klass='tree'), data)

    for child_data in state.children(dm.get(data, 'ID')):
        _generate_tree_item(state, child_data, tag.div(klass='tree-indent'), key=key)

#--------------------------------------------------
# item pages

def _generate_item_page(state, data):
    name = dm.get(data, 'NAME', '?')
    logging.debug('Generating "%s"', name)
    root, tag = _make_page_base(name)

    # basic
    tag.h2('Basics')
    tbl = tag.table()
    for key in ['NAME', 'ID', 'PRIORITY']:
        title = key[0] + key[1:].lower()
        tr = tbl.tr()
        tr.th(title)
        tr.td(dm.get(data, key, '?'))
    tr = tbl.tr()
    tr.th('Status')
    tr.td(dm.get_status(data))
    tr = tbl.tr()
    tr.th('Assigned')
    tr.td(', '.join(filter(len, data.get('ASSIGNED', []))))

    # links
    tag.h2('Links')
    tbl = tag.table()
    tr = tbl.tr()
    for header in ['Parent', 'Child', 'Related']:
        tr.th(header, width='33%')

    parents = [state.get(key)
               for key in dm.get_links(data, 'PARENT')]
    children = state.children(dm.get(data, 'ID'))
    related = [state.get(key)
               for key in dm.get_links(data, 'LINK')]

    for i in range(max(map(len, [parents, children, related]))):
        tr = tbl.tr()
        for items in [parents, children, related]:
            if len(items) > i:
                _add_link(tr.td(), items[i])
            else:
                tr.td()

    # description
    tag.h2('Description')
    if not dm.null(data, 'DESCRIPTION'):
        div = tag.div(klass='description')
        for line in data.get('DESCRIPTION', []):
            div.text(line)
            div.br()

    # time
    tag.h2('Time')

    tbl = tag.table(klass='small')
    for key, value in [('Original estimate', dm.get_estimate(data)),
                       ('Total time spent', dm.get_time_spent(data)),
                       ('Current remaining time', dm.get_remaining_time(data))]:
        tr = tbl.tr()
        tr.th(key)
        tr.td(str(value))
    tr = tbl.tr()
    tr.th('Status')
    _make_relative_meter(tr.td(),
                         -dm.get_projected_time_diff(data),
                         dm.get_estimate(data))

    tag.br()

    tbl = tag.table()
    tr = tbl.tr()
    for header in ['Reported', 'User', 'Spent', 'Remaining']:
        tr.th(header)
    for rep in dm.get_time_reports(data):
        tr = tbl.tr()
        for key in ['time', 'user', 'spent', 'remaining']:
            tr.td(rep[key])

    return root
