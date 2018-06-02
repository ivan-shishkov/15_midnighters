import sys
from datetime import datetime, timedelta

import requests
from requests.exceptions import ConnectionError
from pytz import timezone, utc


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


def is_time_after_midnight(timestamp, timezone_info):
    user_timezone = timezone(timezone_info)
    utc_time = datetime.fromtimestamp(timestamp, utc)
    user_time = utc_time.astimezone(user_timezone)

    midnight_time = datetime(
        year=user_time.year,
        month=user_time.month,
        day=user_time.day,
        tzinfo=user_time.tzinfo,
    )
    return midnight_time < user_time < midnight_time + timedelta(hours=6)


def get_midnighters_info(solution_attempts_info):
    midnighters_info = set()

    for solution_attempt_info in solution_attempts_info:
        timestamp = solution_attempt_info['timestamp']
        username = solution_attempt_info['username']
        timezone_info = solution_attempt_info['timezone']

        if is_time_after_midnight(timestamp, timezone_info):
            midnighters_info.add(username)

    return midnighters_info


def main():
    print('Getting info about solution attempts...')

    solution_attempts_info = get_solution_attempts_info()

    if solution_attempts_info is None:
        sys.exit('Could not get info about solution attempts')

    midnighters_info = get_midnighters_info(solution_attempts_info)


if __name__ == '__main__':
    main()
