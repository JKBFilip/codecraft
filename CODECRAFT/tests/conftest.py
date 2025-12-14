# atrapy folderow zeby nie tworzyc nowego usera
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.auth.user_account import UserAccount

@pytest.fixture
def setup_fake_dirs(tmp_path):
    old_acc = UserAccount.ACCOUNTS_DIR
    old_prog = UserAccount.PROGRESS_DIR
    old_ach = UserAccount.ACHIEVEMENTS_DIR

    UserAccount.ACCOUNTS_DIR = str(tmp_path / "accounts")
    UserAccount.PROGRESS_DIR = str(tmp_path / "progress")
    UserAccount.ACHIEVEMENTS_DIR = str(tmp_path / "achievements")

    yield tmp_path

    UserAccount.ACCOUNTS_DIR = old_acc
    UserAccount.PROGRESS_DIR = old_prog
    UserAccount.ACHIEVEMENTS_DIR = old_ach