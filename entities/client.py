import datetime
import uuid
import cv2
import os

class Client:
  def __init__(self):
    self.id = uuid.uuid4()
    self.entry_date_time = datetime.datetime.now()
    self.image = None
    self.image_position = None
    self.last_seen = datetime.datetime.now()
    self.time_spent = datetime.timedelta(seconds=0)
    self.tags = []

  def __eq__(self, other):
        return other and self.id == other.id

  def is_client_exited(self):
    if (self.last_seen < datetime.datetime.now() - datetime.timedelta(seconds=5)):
        return True
    else:
        return False

  def remove_temp_image(self):
      if self.image == None:
        return

      print(f"Removing temp image {self.image}")
      os.remove(self.image)

  def save_today_image(self):
    if self.image == None:
        return

    today = datetime.date.today()

    date = datetime.date.strftime(today, "%d-%m-%Y")
    month = datetime.date.strftime(today, "%m-%Y")

    image = cv2.imread(self.image)
    cv2.imwrite(f'./images/{month}/{date}/{self.id}.jpg', image)

  def enter(self):
    self.entry_date_time = datetime.datetime.now()

  def calc_time_spent(self):
    if self.entry_date_time == None or self.last_seen == None:
      self.time_spent = datetime.timedelta(seconds=0)
    else:
      self.time_spent = self.last_seen - self.entry_date_time

    return self.time_spent

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

  def to_json(self):
    return {
      "_id": self.id,
      "entry_date_time": self.entry_date_time.strftime("%d-%m-%Y %H:%M:%S") if self.entry_date_time != None else "",
      "last_seen": self.last_seen.strftime("%d-%m-%Y %H:%M:%S") if self.last_seen != None else "",
      "time_spent_in_seconds": self.time_spent.total_seconds(),
      "tags": self.tags
    }
