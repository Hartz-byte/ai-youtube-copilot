import os
import git
import shutil
import tempfile

def load_github_repo(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    git.Repo.clone_from(repo_url, temp_dir, depth=1)
    return temp_dir
