import os
import collections
from utils import get_top_words


def print_calc_result(_project, verb_size, words):

        print('%s: total %s words, %s unique' % (_project, len(words), len(set(words))))
        for word, occurence in collections.Counter(words).most_common(verb_size):
            print(word, occurence)


def calc_verbs(_project: str, verb_size: int):

    project_path = os.path.join('.', _project)
    if not os.path.exists(project_path):
        return

    words = get_top_words(project_path, only_func_names=True, only_verbs=False)
    if words:
        print_calc_result(_project, verb_size, words)


if __name__ == '__main__':
    # TODO Need add some logging

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
        calc_verbs(project, TOP_SIZE)
