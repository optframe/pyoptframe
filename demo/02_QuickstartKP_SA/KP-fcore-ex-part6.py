
class NSBitFlip(object):
    @staticmethod
    def randomMove(pKP: ExampleKP, sol: SolutionKP) -> MoveBitFlip:
        import random
        return MoveBitFlip(random.randint(0, pKP.n - 1))

assert isinstance(NSBitFlip, XNS)     # composition tests
