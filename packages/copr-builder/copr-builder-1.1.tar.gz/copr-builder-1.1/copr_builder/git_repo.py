import logging
import os
import tempfile

from .utils import run_command
from .errors import GitError

log = logging.getLogger("copr.builder")


# username used for git merge
GIT_USER = "CoprBuilderBot"


class GitRepo(object):

    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.tempdir = tempfile.TemporaryDirectory()

        self.gitdir = None

    def clone(self):
        command = 'git clone %s' % self.repo_url
        ret, out = run_command(command, self.tempdir.name)
        if ret != 0:
            raise GitError('Failed to clone %s:\n%s' % (self.repo_url, out))

        subdirs = os.listdir(self.tempdir.name)
        if len(subdirs) != 1:
            raise GitError('Git directory not found after successful clone.')

        self.gitdir = self.tempdir.name + '/' + subdirs[0]

    def last_commit(self, short=True):
        command = 'git log --perl-regexp --author=\'^((?!%s).*)$\' ' \
                  '--pretty=format:\'%%%s\' -n 1' % (GIT_USER, 'h' if short else 'H')
        ret, out = run_command(command, self.gitdir)
        if ret != 0:
            raise GitError('Failed to get last commit hash for %s:\n%s' % (self.repo_url, out))

        return out

    def last_tag(self):
        command = 'git tag -l --sort=taggerdate | tail -n 1'
        ret, out = run_command(command, self.gitdir)
        if ret != 0:
            raise GitError('Failed to get last tag for %s:\n%s' % (self.repo_url, out))

        return out

    def checkout(self, branch):
        command = 'git checkout %s' % branch
        ret, out = run_command(command, self.gitdir)
        if ret != 0:
            raise GitError('Failed to checkout branch %s:\n%s' % (branch, out))

    def merge(self, branch):
        # we need to set username and email to make git happy before merging
        command = 'git config user.email "%s@example.com" && '\
                  'git config user.name "%s"' % (GIT_USER.lower(), GIT_USER)
        ret, out = run_command(command, self.gitdir)
        if ret != 0:
            raise GitError('Failed to set username and email before merging.\n%s' % out)

        command = 'git merge --ff origin/%s' % branch
        ret, out = run_command(command, self.gitdir)
        if ret != 0:
            raise GitError('Failed to merge brach %s:\n%s' % (branch, out))
