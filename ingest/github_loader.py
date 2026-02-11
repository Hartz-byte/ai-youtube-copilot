import subprocess
import tempfile
import shutil
import os
import time
import stat

def load_github_repo(repo_url):
    tmp_dir = tempfile.mkdtemp()

    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, tmp_dir],
        check=True
    )

    return tmp_dir

def _handle_remove_readonly(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def cleanup_repo(path):
    time.sleep(1)
    shutil.rmtree(path, onerror=_handle_remove_readonly)
