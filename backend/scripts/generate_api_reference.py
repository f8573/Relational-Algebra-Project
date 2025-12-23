"""Generate API reference by extracting docstrings from app/api and app/services.

Usage:
    python backend/scripts/generate_api_reference.py

This script writes `backend/docs/API_REFERENCE_AUTOGEN.md`.
"""

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_PATHS = [ROOT / 'app' / 'api', ROOT / 'app' / 'services']
OUT_FILE = ROOT / 'docs' / 'API_REFERENCE_AUTOGEN.md'


def format_args(node: ast.FunctionDef) -> str:
    parts = []
    args = node.args
    # positional args (skip self)
    pos = [a.arg for a in args.args]
    if pos and pos[0] == 'self':
        pos = pos[1:]
    parts.extend(pos)
    # vararg
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    # kwonly args
    for a in args.kwonlyargs:
        parts.append(a.arg)
    # kwarg
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    return ', '.join(parts)


def extract_from_file(path: Path):
    text = path.read_text(encoding='utf8')
    module = ast.parse(text)
    mod_doc = ast.get_docstring(module) or ''

    items = []
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            name = node.name
            sig = format_args(node)
            doc = ast.get_docstring(node) or ''
            # Extract Flask route decorator info if present
            route_info = []
            for dec in node.decorator_list:
                # looking for patterns like @bp.route('/path', methods=['POST'])
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    if dec.func.attr == 'route':
                        path_arg = None
                        methods = None
                        # positional first arg is the route string
                        if dec.args:
                            a0 = dec.args[0]
                            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                                path_arg = a0.value
                        # look for methods kwarg
                        for kw in dec.keywords:
                            if kw.arg == 'methods':
                                # kw.value should be a list of constants
                                if isinstance(kw.value, (ast.List, ast.Tuple)):
                                    methods = []
                                    for el in kw.value.elts:
                                        if isinstance(el, ast.Constant) and isinstance(el.value, str):
                                            methods.append(el.value)
                        route_info.append({'path': path_arg, 'methods': methods})

            items.append(('function', name, sig, doc, route_info))
        elif isinstance(node, ast.ClassDef):
            cname = node.name
            cdoc = ast.get_docstring(node) or ''
            methods = []
            for m in node.body:
                if isinstance(m, ast.FunctionDef):
                    mname = m.name
                    msig = format_args(m)
                    mdoc = ast.get_docstring(m) or ''
                    methods.append((mname, msig, mdoc))
            items.append(('class', cname, cdoc, methods))
    return mod_doc, items


def walk_and_extract(paths):
    collected = []
    for base in paths:
        for root, dirs, files in os.walk(base):
            # skip __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if not f.endswith('.py'):
                    continue
                p = Path(root) / f
                rel = p.relative_to(ROOT)
                mod_doc, items = extract_from_file(p)
                collected.append((str(rel), mod_doc, items))
    return collected


def render_md(collected):
    lines = []
    lines.append('# Auto-generated API Reference')
    lines.append('')
    lines.append('This file is generated from the docstrings in `app/api` and `app/services`.')
    lines.append('')

    for rel, mod_doc, items in sorted(collected):
        lines.append(f'## Module: {rel}')
        lines.append('')
        if mod_doc:
            lines.append(mod_doc)
            lines.append('')
        for it in items:
            if it[0] == 'function':
                _, name, sig, doc, route_info = it
                header = f'### Function: `{name}({sig})`'
                if route_info:
                    # show routes inline
                    routes = []
                    for r in route_info:
                        pm = ''
                        if r.get('methods'):
                            pm = f" [{', '.join(r['methods'])}]"
                        routes.append(f"{r.get('path') or '<dynamic>'}{pm}")
                    header += ' — routes: ' + ', '.join(routes)

                lines.append(header)
                lines.append('')
                if doc:
                    lines.append(doc)
                    lines.append('')
            elif it[0] == 'class':
                _, cname, cdoc, methods = it
                lines.append(f'### Class: `{cname}`')
                lines.append('')
                if cdoc:
                    lines.append(cdoc)
                    lines.append('')
                for mname, msig, mdoc in methods:
                    lines.append(f'- `{mname}({msig})`')
                    if mdoc:
                        # keep brief one-line doc
                        one = mdoc.strip().splitlines()[0]
                        lines.append(f'  - {one}')
                lines.append('')
    return '\n'.join(lines)


def main():
    collected = walk_and_extract(API_PATHS)
    md = render_md(collected)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(md, encoding='utf8')
    print('Wrote', OUT_FILE)


if __name__ == '__main__':
    main()
