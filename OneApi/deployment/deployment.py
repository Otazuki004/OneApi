from .. import *
from . import Methods 
from ..database import user

class Deployment(Methods):
  def __init__(self):
    self.lf = "\n[ElevenHost]"
    self.database = user()
