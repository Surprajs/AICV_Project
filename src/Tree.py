class Tree:
    
    def __init__(self, val, parent=None):
        self.parent = parent
        self.val = val
        self.children = list()


    def add_child(self, val):
        self.children.append(Tree(val, self))
        return self.children[-1]
    
    def get_value(self):
        return self.val
    
    def set_value(self, new_val):
        self.val = new_val

    def get_parent(self):
        return self.parent

    def get_child(self, idx):
        return self.children[idx]

    def remove_child(self, child_idx):
        del self.children[child_idx]

    def get_children(self):
        return self.children

    def is_root(self):
        return not self.parent

    def is_external(self):
        return  not self.children
        
if __name__ == "__main__":
    t1 = Tree(5)
    

