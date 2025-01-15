from .user_info import UserInfo
from .get_repos import GetRepos
from .delete_user import DeleteUser
from .disconnect_git import DisconnectGit
from .set_repo import SetRepo
from .add_log import addLog
from .check_repo import CheckRepo

class Methods(
  UserInfo,
  GetRepos,
  DeleteUser,
  DisconnectGit,
  SetRepo,
  addLog,
  CheckRepo,
):
  pass
