# -*- coding: utf-8 -*-

from bio2bel.utils import build_cli
from .manager import Manager
from .web import get_app

main = build_cli(Manager, create_application=get_app)

if __name__ == '__main__':
    main()
