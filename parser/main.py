import requests
import psycopg2
import os

GITHUB_API_BASE_URL = 'https://api.github.com'


def fetch_github_top_repositories() -> list:
    try:
        path = "/search/repositories"
        url = GITHUB_API_BASE_URL + path
        params = {
            "q": "stars:>1",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": 1,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        res = response.json()

        if "items" not in res:
            raise KeyError(f"Wrong GitHub API response: {res}")
        return res.get('items')
    except requests.exceptions.HTTPError as http_err:
        print(f'GitHub API HTTP error: {http_err}')
    except Exception as err:
        print(f'Failed to fetch GitHub repositories: {err}')

def save_github_top_repositories(repositories: list) -> None:
    try:
        with psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        ) as connection:
            with connection.cursor() as cursor:
                for position_cur, repo in enumerate(repositories, start=1):
                    cursor.execute("""
                        INSERT INTO repositories 
                            (repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language)
                        VALUES 
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (repo) DO UPDATE
                        SET position_prev = repositories.position_cur,
                            position_cur = EXCLUDED.position_cur,
                            stars = EXCLUDED.stars,
                            watchers = EXCLUDED.watchers,
                            forks = EXCLUDED.forks,
                            open_issues = EXCLUDED.open_issues,
                            language = EXCLUDED.language
                        ;
                    """, (
                        repo['full_name'],
                        repo['owner']['login'],
                        position_cur,
                        None,
                        repo['stargazers_count'],
                        repo['watchers_count'],
                        repo['forks_count'],
                        repo['open_issues_count'],
                        repo['language']
                    ))
    except Exception as err:
        print(f'Failed to save GitHub repositories to db: {err}')

def parse_github_top_repositories():
    try:
        repositories = fetch_github_top_repositories()
        save_github_top_repositories(repositories)
    except Exception as err:
        print(f'Failed to parse top 100 GitHub repositories: {err}')
