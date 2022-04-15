import block

class DropoffBlock(block.Block):
    def increase_block_count(self):
        self.block_count += 1