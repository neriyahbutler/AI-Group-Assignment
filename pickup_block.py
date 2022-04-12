import block

class PickupBlock(block.Block):
    def decrease_count(self):
        self.count -= 1