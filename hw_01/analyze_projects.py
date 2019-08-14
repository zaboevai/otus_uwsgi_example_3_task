import os
import collections
from hw_01.utils import get_top_verbs


def print_calc_result(_project, verb_size, words):
    if words:
        print('%s: total %s words, %s unique' % (_project, len(words), len(set(words))))
        for word, occurence in collections.Counter(words).most_common(verb_size):
            print(word, occurence)


def calc_verbs(_project: str, verb_size: int):

    project_path = os.path.join('.', _project)
    if not os.path.exists(project_path):
        return

    words = get_top_verbs(project_path)
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
