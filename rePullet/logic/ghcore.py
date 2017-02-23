import github
from github.Issue import Issue
from github.PullRequest import PullRequest
from github import Github
from urllib.parse import urlparse
import os.path

from rePullet.logic.user import User

#github.enable_console_debug_logging()

def count_rebuild(issue, pull):
    """
    @type issue: Issue
    @type pull: PullRequest
    """
    rebuild = 0
    if pull.comments != 0:
        issuecomments = issue.get_comments()
        pullcommits = pull.get_commits()
        startcomment = issuecomments[0]
        for comment in issuecomments:
            for commit in pullcommits:
                if startcomment.created_at < commit.commit.committer.date < comment.created_at:
                    rebuild += 1  # защитывается только одна доделка
                    break
            startcomment = comment
        for commit in pullcommits:
            if commit.commit.committer.date > startcomment.created_at:
                rebuild += 1
                break
    return rebuild


def countReport(pull):
    """
    :param pull: PullRequest
    :type pull: PullRequest
    :return: bool
    """
    count = 0
    for fl in pull.get_files():
        if (fl.filename.endswith(".pdf")
            or fl.filename.endswith(".doc")
            or fl.filename.endswith(".docx")):
            count += 1
    return count

def getUserData(access_token):
    try:
        ghI = Github(login_or_token=access_token, timeout=15)
        user = ghI.get_user()
        print(user)
        name = user.login
        avatar = user.avatar_url
        userid = user.id
        return User(userid, ghI, name, avatar)
    except github.GithubException:
        print('lol')

def is_repo_owner(urlstr, user):
    path = urlparse(urlstr).path
    os.path.split(path)
    while os.path.dirname(path) != '/':
        path = os.path.dirname(path)
    name = path[1:]
    return True if user.name == name else False

def getrepoid(user, url):
    # TODO: проверка url на валидность
    path = urlparse(url).path
    prev = ''
    while os.path.dirname(path) != '/':
        prev = path
        path = os.path.dirname(path)
    path = prev[1:]
    repo = user.ghI.get_repo(path)
    if repo:
        return repo.id
    return None
