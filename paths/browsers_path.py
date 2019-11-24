import re, os


def full_paths(paths):
    env = re.compile(r'{(\w*)}')
    full_paths = []
    for path in paths:
        replace_with_env = env.search(path)
        full_path = path.replace(replace_with_env.group(), os.getenv(replace_with_env.group(1)))
        full_paths.append(full_path)
    return(full_paths)
