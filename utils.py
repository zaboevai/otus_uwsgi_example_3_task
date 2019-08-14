import ast
import collections
import os

import nltk
from git import Repo


def clone_github_repo(repo_path, dir_path):
    """
    Clone GITHUB repositories to dir
    :param repo_path:
    :param dir_path:
    :return:
    """
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
    pos_info = nltk.pos_tag(_word)
    return pos_info[0][1] == 'VB'


def get_trees_from_path(path: str, with_file_names: bool = False, with_file_content: bool = False) -> list:
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

        if not tree:
            continue

        if with_file_names:
            trees.append((file_name, tree))
            if with_file_content:
                trees.append((file_name, file_content, tree))
        else:
            trees.append(tree)

    return trees


def get_names_from_tree(tree: list, func_names=False) -> list:
    """
    Get function names from Abstract Syntax Trees
    :param func_names:
    :param tree:    ast tree
    :return:        list of func names
    """
    if func_names:
        res = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    else:
        res = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]

    return res


def split_snake_case_name_to_words(name: str) -> list:
    """
    make a list of words without '_'
    :param name:
    :return:
    """
    return [name_word for name_word in name.split('_')]


def get_all_words_from_path(path: str, only_func_names: bool = False) -> list:
    """
    Get all words or func names from path
    :param path:
    :param only_func_names:
    :return:
    """

    trees = get_trees_from_path(path)

    for tree in trees:
        names = (get_names_from_tree(tree=tree, func_names=only_func_names))

    user_names = [name for name in names if
                  not (name.startswith('__') and name.endswith('__'))]

    return make_flat([split_snake_case_name_to_words(user_name) for user_name in user_names])


def get_top_words(path: str, top_size: int = 10, only_func_names=False, only_verbs=False) -> list:
    """
    Get top verbs in path with specified size
    :param only_func_names:
    :param path:        path to file
    :param top_size:    size of verb
    :return:            list of verbs
    """
    names = get_all_words_from_path(path=path, only_func_names=only_func_names)

    if only_verbs:
        names = [name for name in names if is_verb(name)]

    return collections.Counter(names).most_common(top_size)
