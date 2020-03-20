import os
import json
import datetime
import argparse
import requests
import jinja2


# all relative to project root
TEMPLATES_DIR_PATH = './src/templates'
PUBLIC_DIR_PATH = './public'
ARTICLE_DIR_PATH = os.path.join(PUBLIC_DIR_PATH, 'articles')


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR_PATH))


def get_issue_data(repo, issue_id):
    url = f'https://api.github.com/repos/{repo}/issues/{issue_id}'
    print(f'GET {url}')
    resp = requests.get(url)
    return resp.json()


def process_issue(repo, issue_id, cache_dir=None):
    filename_prefix = f'{repo.replace("/", "-")}-{issue_id}'.lower()
    filename = f'{filename_prefix}.html'

    data: dict
    if cache_dir:
        cache_filepath = os.path.join(cache_dir, f'{filename_prefix}.json')
        if os.path.exists(cache_filepath):
            with open(cache_filepath, 'r') as f:
                data = json.load(f)
        else:
            data = get_issue_data(repo, issue_id)
            with open(cache_filepath, 'w') as f:
                json.dump(data, f)
    else:
        data = get_issue_data(repo, issue_id)

    markdown_content = data['body']

    tpl = jinja_env.get_template('github_issue.html')
    html = tpl.render(
        title=f'Github Issue | {repo} | #{issue_id}',
        markdown_content=markdown_content,
        source_url=f'https://github.com/{repo}/issues/{issue_id}',
    )

    print(f'{datetime.datetime.now()} writing to {ARTICLE_DIR_PATH}/{filename}')
    with open(os.path.join(ARTICLE_DIR_PATH, filename), 'w') as f:
        f.write(html)


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(description="", epilog="", formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('repo', metavar="REPO", type=str, help="github repo path, e.g. reorx/httpstat")
    parser.add_argument('issue_id', metavar="ISSUE", type=str, help="issue id")

    parser.add_argument('--cache-dir', type=str, help="cache dir, if cache file exists, no request will be made")

    args = parser.parse_args()

    process_issue(args.repo, args.issue_id, cache_dir=args.cache_dir)


if __name__ == '__main__':
    main()
