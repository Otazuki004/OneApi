from .user_info import UserInfo
from .get_repos import GetRepos
from .delete_user import DeleteUser
from .disconnect_git import DisconnectGit
from .set_repo import SetRepo
from .add_log import addLog
from .get_repo import GetRepo

class Methods(
  UserInfo,
  GetRepos,
  DeleteUser,
  DisconnectGit,
  SetRepo,
  addLog,
  GetRepo,
):
  pass
