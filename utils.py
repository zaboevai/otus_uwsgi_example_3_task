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
        elif with_file_content:
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
    ast_instance = ast.FunctionDef if func_names else ast.Name
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast_instance)]


def split_snake_case_name_to_words(name: str, verbs=False) -> list:
    """
    Get verbs from function name
    :param name:
    :return: list of words
    """
    # TODO РАЗБИТЬ на 2 либо сплит вынести
    verb_words = []
    words = []

    name_words = [name_word for name_word in name.split('_')]
    for name_word in name_words:
        if is_verb(name_word):
            verb_words.append(name_word)
        else:
            words.append(name_word)

    return verb_words if verbs else words


# def get_all_names_from_tree(tree):
#     return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_words_from_path(path, func_names=True):
    trees = get_trees_from_path(path)
    names = []
    for tree in trees:
        names.append(get_names_from_tree(tree=tree, func_names=func_names))

    # TODO возможно есть лишний make_flat
    names = make_flat(names)
    user_names = [name for name in names if
                  not (name.startswith('__') and name.endswith('__'))]
    # TODO возможно есть лишний make_flat
    return make_flat([split_snake_case_name_to_words(user_name) for user_name in user_names])


# def get_func_name_from_path(path: str) -> list:
#     """
#     Get function names in path
#     :param path:        path to file
#     :return:            list of function names
#     """
#     trees = get_trees_from_path(path)
#     func_names = make_flat([get_names_from_tree(tree=tree, func_names=True) for tree in trees])
#     user_func_names = [func_name for func_name in func_names
#                        if not (func_name.startswith('__') and func_name.endswith('__'))]
#     return user_func_names


def get_top_func_names(path: str, top_size: int = 10) -> list:
    """
    Get top function names in path with specified size
    :param path:        path to file
    :param top_size:    size of function names
    :return:            list of function names
    """
    func_names = get_all_words_from_path(path=path, func_names=True)
    return collections.Counter(func_names).most_common(top_size)


def get_top_verbs(path: str, top_size: int = 10, func_names=False) -> list:
    """
    Get top verbs in path with specified size
    :param func_names:
    :param path:        path to file
    :param top_size:    size of verb
    :return:            list of verbs
    """

    names = get_all_words_from_path(path=path, func_names=func_names)

    verbs = make_flat([split_snake_case_name_to_words(name, verb_words=True) for name in names])
    return collections.Counter(verbs).most_common(top_size)
