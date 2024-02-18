import datetime as dt


class Note:

    def __init__(self, id_note, title_note, text_note, new_datetime_note=""):
        self.id = id_note  # идентификатор
        self.title = title_note  # заголовок
        self.text = text_note  # тело заметки
        if new_datetime_note is None:
            self.datetime_note = dt.datetime.now()  # дата/время создания заметки
        else:
            self.datetime_note = new_datetime_note  # дата/время последнего изменения заметки

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def get_datetime(self):
        return self.datetime_note

    def set_id(self, id_note):
        self.id = id_note

    def set_title(self, title_note):
        self.title = title_note
        self.datetime_note = dt.datetime.now()

    def set_text(self, text_note):
        self.text = text_note
        self.datetime_note = dt.datetime.now()

    def set_datetime(self, datetime_note):
        self.datetime_note = datetime_note

    def __str__(self):
        return f"Заметка №{self.id} от {self.datetime_note}: '{self.title}'\n>>>'{self.text}'"
