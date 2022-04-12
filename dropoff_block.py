import block

class DropoffBlock(block.Block):
    def increase_count(self):
        self.count += 1