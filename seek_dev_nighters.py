import sys

import requests
from requests.exceptions import ConnectionError


def execute_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
    except ConnectionError:
        return None

    return response.json() if response.ok else None


def get_solution_attempts_info():
    solution_attempts_info = []

    page_number = 1

    while True:
        solution_attempts_info_page = execute_get_request(
            url='https://devman.org/api/challenges/solution_attempts',
            params={
                'page': page_number,
            },
        )
        if solution_attempts_info_page is None:
            return None

        solution_attempts_info.extend(solution_attempts_info_page['records'])

        if page_number >= solution_attempts_info_page['number_of_pages']:
            return solution_attempts_info

        page_number = page_number + 1


def main():
    print('Getting info about solution attempts...')

    solution_attempts_info = get_solution_attempts_info()

    if solution_attempts_info is None:
        sys.exit('Could not get info about solution attempts')


if __name__ == '__main__':
    main()
