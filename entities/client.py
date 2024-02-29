import datetime

class Client:
  def __init__(self, id):
    self.id = id
    self.entry_date_time = None
    self.left_date_time = None
    self.image = None
    self.image_position = None
    self.last_seen = datetime.datetime.now()
    self.tags = []

  def __eq__(self, other):
        return other and self.id == other.id

  def is_client_exited(self):
    if (self.last_seen < datetime.datetime.now() - datetime.timedelta(seconds=5)):
        return True
    else:
        return False

  def enter(self):
    self.entry_date_time = datetime.datetime.now()

  def left(self):
    self.left_date_time = datetime.datetime.now()

  def get_time_spent(self):
    if self.left_date_time == None:
        return False

  def set_image (self, image):
    self.image = image

  def set_last_seen(self):
    self.last_seen = datetime.datetime.now()

  def set_tags(self, tags):
    self.tags = tags

  def set_tag(self, tag):
    if tag in self.tags:
      return
    else:
      self.tags.append(tag)

  def set_image_position(self, position):
    self.image_position = position
