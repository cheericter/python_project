# -*- coding: utf-8 -*-
import sys
import re
from handlers import *
from rules import *
from util import *


class Parse:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addrule(self, rule):
        self.rules.append(rule)

    def addfilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern,handler.sub(name),block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end('document')


class BasicTextParse(Parse):
    def __init__(self, handler):
        Parse.__init__(self, handler)
        self.addrule(ListRule())
        self.addrule(ListitemRule())
        self.addrule(TitleRule())
        self.addrule(HeadingRules())
        self.addrule(ParagraphRule())

        self.addfilter(r'\*(.+?)\*', 'emphasis')
        self.addfilter(r'(http://[/\.a-zA-Z]+)', 'url')
        self.addfilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')
if __name__ == "__main__":
    handler = HTMLRender()
    parser = BasicTextParse(handler)
    parser.parse(sys.stdin)
