import requests
from requests.exceptions import ConnectionError


def execute_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
    except ConnectionError:
        return None

    return response.json() if response.ok else None


def main():
    pass


if __name__ == '__main__':
    main()
