from part1 import build_tree, parse_commands

def get_total_size(directory):
    my_size = 0
    for subdir in directory.subdirs.values():
        my_size += get_total_size(subdir)
    for subfile in directory.subfiles.values():
        my_size += subfile.file.size
    return my_size

def get_candidates(directory):
    for subdir in directory.subdirs.values():
        yield from get_candidates(subdir)
    yield get_total_size(directory), directory
    
def get_size_of_directory_to_delete(directory):
    total_size = get_total_size(directory)
    need_to_delete = total_size - (70000000 - 30000000)
    assert need_to_delete > 0
    
    deleted, dirnode = min(
        (size, dirnode) for size, dirnode in get_candidates(directory)
        if size >= need_to_delete
    )
    assert deleted >= need_to_delete
    return deleted

if __name__ == "__main__":
    root = build_tree(parse_commands())
    root.pretty_print()
    print(get_size_of_directory_to_delete(root))
