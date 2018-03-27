# -*- coding: utf-8 -*-

from bio2bel.utils import build_cli
from .manager import Manager

main = build_cli(Manager)

if __name__ == '__main__':
    main()
