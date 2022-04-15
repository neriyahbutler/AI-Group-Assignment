import block

class PickupBlock(block.Block):
    def decrease_block_count(self):
        self.block_count -= 1
