import ast
import collections
import os
from git import Repo

from nltk import pos_tag as nltk_pos_tag


def clone_github_repo(repo_path, dir_path):
    Repo.clone_from(url=repo_path, to_path=dir_path)


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
    pos_info = nltk_pos_tag(_word)
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

    for file_name in file_names:

        with open(file=file_name, mode='r', encoding='utf-8') as file:
            file_content = file.read()

        try:
            tree = ast.parse(file_content)
        except SyntaxError as exc:
            raise exc

        if with_file_names:
            if with_file_content:
                trees.append((file_name, file_content, tree))
            else:
                trees.append((file_name, tree))
        else:
            trees.append(tree)

    return trees


def get_func_name_from_tree(tree: list) -> list:
    """
    Get function names from Abstract Syntax Trees
    :param tree:    ast tree
    :return:        list of func names
    """
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_verbs_from_function_name(function_name: str) -> list:
    """
    Get verbs from function name
    :param function_name:
    :return: list of verbs
    """
    return [verb_word for verb_word in function_name.split('_') if is_verb(verb_word)]


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

    verbs = make_flat([get_verbs_from_function_name(user_func_name) for user_func_name in user_func_names])
    return collections.Counter(verbs).most_common(top_size)
