import sys
from dataclasses import dataclass
from typing import List

@dataclass
class File:
    name: str
    size: int

@dataclass
class LSCommand:
    directories: List[str]
    files: List[File]

@dataclass
class CDCommand:
    path: str

def parse_commands():
    ls_dirs = None
    ls_files = None
    state = 0
    for line in sys.stdin:
        line = line.strip().split(" ")
        if not line:
            break
        while True:
            if state == 0:
                assert line[0] == "$"
                if line[1] == "ls":
                    ls_dirs = []
                    ls_files = []
                    state = 1
                elif line[1] == "cd":
                    yield CDCommand(line[2])
                else:
                    assert False
                break
            elif state == 1:
                if line[0] == "$":
                    state = 0
                    yield LSCommand(ls_dirs, ls_files)
                    continue
                elif line[0] == "dir":
                    ls_dirs.append(line[1])
                else:
                    ls_files.append(File(line[1], size=int(line[0])))
                break
            else:
                assert False
    if state == 1:
        yield LSCommand(ls_dirs, ls_files)

class FileNode:
    def __init__(self, file, parent):
        self.file = file
        self.parent = parent

    def __str__(self):
        rev = []
        cur = self.parent
        while cur != None:
            rev.append(cur.name or "")
            cur = cur.parent
        rev = rev[::-1]
        rev.append(self.file.name)
        return f"<File {'/'.join(rev)} of size {self.file.size}>"

class DirectoryNode:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.subdirs = {}
        self.subfiles = {}

    def __str__(self):
        rev = []
        cur = self
        while cur != None:
            rev.append(cur.name or "")
            cur = cur.parent
        return f"<Directory {'/'.join(rev[::-1]) if len(rev) > 1 else '/'}>"

    def find_root(self):
        if self.parent is None:
            return self
        return self.parent.find_root()

    def touch_local_file(self, file):
        if file.name not in self.subfiles:
            self.subfiles[file.name] = FileNode(file, parent=self)
        return self.subfiles[file.name]

    def touch_local_dir(self, name):
        assert "/" not in name
        if name not in self.subdirs:
            self.subdirs[name] = DirectoryNode(name=name, parent=self)
        return self.subdirs[name]

    def touch_absolute_dir(self, path):
        root = self.find_root()
        if path == "/":
            return root
        assert path.startswith("/")
        cur = root
        for name in path.split("/")[1:]:
            cur = cur.touch_local_dir(name)
        return cur

    def pretty_print(self, indent=0):
        indenting = "  " * indent
        print(f"{indenting}dir {self.name or '/'}")
        for name, node in self.subdirs.items():
            node.pretty_print(indent=indent+1)
        for name, node in self.subfiles.items():
            print(f"{indenting}  {name} of size {node.file.size}")
        


def build_tree(commands):
    root = DirectoryNode()
    cwd = root
    for command in commands:
        if isinstance(command, CDCommand):
            if command.path.startswith("/"):
                cwd = root.touch_absolute_dir(command.path)
            elif command.path == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.touch_local_dir(command.path)
        elif isinstance(command, LSCommand):
            for directory in command.directories:
                cwd.touch_local_dir(directory)
            for file in command.files:
                cwd.touch_local_file(file)
    return root


def get_total_directory_size_below_thresh(directory):
    my_size = 0
    my_total = 0
    for subdir in directory.subdirs.values():
        sub_size, sub_total = get_total_directory_size_below_thresh(subdir)
        my_size += sub_size
        my_total += sub_total
    for subfile in directory.subfiles.values():
        my_size += subfile.file.size
    if my_size <= 100000:
        my_total += my_size
    return my_size, my_total
    

if __name__ == "__main__":
    root = build_tree(parse_commands())
    root.pretty_print()
    print(get_total_directory_size_below_thresh(root)[1])
