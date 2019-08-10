import ast
import os
import collections

from nltk import pos_tag


def make_flat(_list: list) -> list:
    """
    Make the list flat
    :param _list:       SOURCE LIST
    :return: list       FLAT LIST

    example: [(1,2), (3,4)] -> [1, 2, 3, 4]
    """
    return sum([list(item) for item in _list], [])


def is_verb(_word: str) -> bool:
    """
    Check on verb word
    :param _word:       WORD
    :return: boolean    BOOLEAN RESULT
    """
    if not _word:
        return False
    pos_info = pos_tag(_word)
    return pos_info[0][1] == 'VB'


def get_trees(path: str, with_file_names: bool = False, with_file_content: bool = False) -> list:
    """
    Create list of Abstract Syntax Trees from file content
    :param path:                PATH TO FILE
    :param with_file_names:     TREE WITH FILE NAME
    :param with_file_content:   TREE WITH FILE CONTENT
    :return:                    LIST OF AST TREE
    """

    file_names = []
    trees = []

    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) == 100:
                    break

    print('total %s files' % len(file_names))

    for file_name in file_names:

        with open(file_name, 'r', encoding='utf-8') as file:
            file_content = file.read()

        try:
            tree = ast.parse(file_content)
        except SyntaxError as exc:
            print(exc)
            tree = None

        if with_file_names:
            if with_file_content:
                trees.append((file_name, file_content, tree))
            else:
                trees.append((file_name, tree))
        else:
            trees.append(tree)

    print('trees generated')
    return trees


def get_func_name_from_tree(tree: list) -> list:
    """
    Get function names from Abstract Syntax Trees
    :param tree:    ast tree
    :return:        list of func names
    """
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


#
# def get_all_names(tree):
#     return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name: str) -> list:
    """
    Get verbs from function name
    :param function_name:
    :return: list of verbs
    """
    return [verb_word for verb_word in function_name.split('_') if is_verb(verb_word)]


# def get_all_words_in_path(path):
#     trees = [t for t in get_trees(path) if t]
#     function_names = [f for f in flat([get_all_names(t) for t in trees]) if
#                       not (f.startswith('__') and f.endswith('__'))]
#
#     def split_snake_case_name_to_words(name):
#         return [n for n in name.split('_') if n]
#
#     return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_top_verbs_in_path(path: str = None, top_size: int = 10) -> list:
    """
    Get top verbs in path with specified size
    :param path:        path to file
    :param top_size:    size of verb
    :return:            list of verbs
    """

    trees = [tree for tree in get_trees(path) if tree]
    func_names = make_flat(list(get_func_name_from_tree(tree) for tree in trees))
    user_func_names = [func_name for func_name in func_names
                       if not (func_name.startswith('__') and func_name.endswith('__'))]
    print('functions extracted')
    verbs = make_flat([get_verbs_from_function_name(user_func_name) for user_func_name in user_func_names])
    return collections.Counter(verbs).most_common(top_size)


# def get_top_functions_names_in_path(path, top_size=10):
#     t = get_trees(path)
#     nms = [f for f in
#            flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if
#            not (f.startswith('__') and f.endswith('__'))]
#     return collections.Counter(nms).most_common(top_size)


def calc_verbs_in_project(_project: str, verb_size: int):
    project_path = os.path.join('.', _project)
    words = get_top_verbs_in_path(project_path)
    print('%s: total %s words, %s unique' % (_project, len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(verb_size):
        print(word, occurence)


if __name__ == '__main__':

    TOP_SIZE = 200

    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        calc_verbs_in_project(project, TOP_SIZE)
