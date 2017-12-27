
class PokerObject:

    # https://stackoverflow.com/a/41454816/4621324
    def _repr_pretty_(self, p, cycle):
        p.text(str(self) if not cycle else '...')