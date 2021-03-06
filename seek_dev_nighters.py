import sys
from datetime import datetime

import requests
from requests.exceptions import ConnectionError
from pytz import timezone


def execute_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        return response.json() if response.ok else None
    except ConnectionError:
        return None


def get_solution_attempts_info():
    page_number = 1

    while True:
        solution_attempts_info_page = execute_get_request(
            url='https://devman.org/api/challenges/solution_attempts',
            params={
                'page': page_number,
            },
        )
        yield solution_attempts_info_page['records']

        if page_number >= solution_attempts_info_page['number_of_pages']:
            break

        page_number = page_number + 1


def is_nighttime_after_midnight(
        timestamp, timezone_info, midnight_hour=0, morning_hour=6):
    user_local_time = datetime.fromtimestamp(
        timestamp,
        tz=timezone(timezone_info),
    )
    return midnight_hour <= user_local_time.hour < morning_hour


def get_midnighters_info(solution_attempts_info):
    midnighters_info = set()

    for solution_attempt_info in solution_attempts_info:
        timestamp = solution_attempt_info['timestamp']
        username = solution_attempt_info['username']
        timezone_info = solution_attempt_info['timezone']

        if is_nighttime_after_midnight(timestamp, timezone_info):
            midnighters_info.add(username)

    return midnighters_info


def print_midnighters_info(midnighters_info):
    print('\nDevman users who send their solutions after midnight:\n')

    if not midnighters_info:
        print('Nobody send their solutions after midnight')
        return

    for midnighter_info in sorted(midnighters_info):
        print(midnighter_info)


def main():
    print('Getting info about solution attempts...')

    midnighters_info = set()

    for solution_attempts_info in get_solution_attempts_info():
        if solution_attempts_info is None:
            sys.exit('Could not get info about solution attempts')

        midnighters_info.update(
            get_midnighters_info(solution_attempts_info),
        )

    print_midnighters_info(
        midnighters_info=midnighters_info,
    )


if __name__ == '__main__':
    main()
