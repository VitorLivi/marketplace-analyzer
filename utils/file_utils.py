import os
import datetime

class FileUtils:
    @staticmethod
    def remove (path):
        os.remove(path)

    @staticmethod
    def remove_all_in_dir (path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    @staticmethod
    def create_today_dir (path):
        date = datetime.date.strftime(datetime.date.today(), "%d-%m-%Y")
        if not os.path.exists(f'{path}/{date}'):
            os.makedirs(f'{path}/{date}')


