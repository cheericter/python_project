# -*- coding: utf-8 -*-


class Rule:
    """
    所有规则的基类
    """
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadingRules(Rule):
    """
        标题最多70个字，并且不以：结尾
    """
    type = 'heading'

    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRules):
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first: return False
        self.first=False
        return HeadingRules.condition(self, block)


class ListitemRule(Rule):
    type = 'listitem'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ListRule (ListitemRule):
    type = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and  ListitemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListitemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    type = 'paragraph'

    def condition(self, block):
        return True


