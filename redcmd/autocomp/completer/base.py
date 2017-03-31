from abc import ABCMeta, abstractmethod


class Op:
    __metaclass__ = ABCMeta
    AND = 0
    OR = 1

    def __and__(self, other):
        return MultiCompleter(self, other, Op.AND)    


    def __or__(self, other):
        return MultiCompleter(self, other, Op.OR)


    @abstractmethod
    def complete(self, term):
        pass


class Completer(Op):

    def complete(self, term):
        pass


class MultiCompleter(Op):

    def __init__(self, op1, op2, op):
        self._op = op
        self._operand1 = op1
        self._operand2 = op2

    def complete(self):
        c1 = self._operand1.complete()
        c2 = self._operand2.complete()

        out = []
        if self._op == Op.AND:
            for c in c1:
                if c in c2:
                    out.append(c)
        elif self._op == Op.OR:
            out = list(set(c1 + c2))
        else:
            pass

        return out


def get_completions(term, completer):
    completions = []

    if completer is not None:
        return completer[0].complete(term)

