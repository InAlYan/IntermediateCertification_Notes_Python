import datetime as dt
import os
import note
import parse_exceptions


class Notes:
    max_id = 0
    datetime_format_string = '%Y-%m-%d'

    def __init__(self):
        self.notes = {}
        Notes.max_id = self.get_max_id()

    def get_max_id(self):
        maxid = 0
        for k, v in self.notes.items():
            if k > maxid:
                maxid = k
        return maxid

    def add_note(self, new_note_title, new_note_text, new_id_note=None, new_datetime_note=None):
        """Добавить заметку, возвращается ключ заметки в словаре (id), если в словаре уже будет заметка с таким
        ключом id она будет перезаписана"""
        if new_id_note is None:
            Notes.max_id += 1
            id_to_write = Notes.max_id
        else:
            id_to_write = new_id_note
        new_note = note.Note(id_to_write, new_note_title, new_note_text, new_datetime_note)
        self.notes[new_note.id] = new_note
        return new_note.id

    def delete_note(self, id_to_delete):
        """Удалить заметку по id_to_delete, возвращается удаленная заметка, еcли заметки не было
        возвращается None"""
        id_delete = self.str_to_int(id_to_delete)
        if not id_delete and id_delete != 0:
            raise parse_exceptions.ParseIntException("Невозможно преобразовать к целому значению:", id_to_delete)
        if self.notes.get(id_delete) is not None:
            return self.notes.pop(id_delete)
        else:
            return None

    def edit_note(self, id_to_edit, new_title="", new_text=""):
        """Редактировать заметку по id_to_edit, возвращается отредактированная заметка, еcли такой заметки нет
        возвращается None"""
        id_edit = self.str_to_int(id_to_edit)
        if not id_edit and id_edit != 0:
            raise parse_exceptions.ParseIntException("Невозможно преобразовать к целому значению:", id_to_edit)
        editable_note = self.notes.get(id_edit)
        if editable_note is not None:
            if new_title != "":
                editable_note.set_title(new_title)
            if new_text != "":
                editable_note.set_text(new_text)
        return editable_note

    def get_note_by_id(self, target_id):
        """Вернуть заметку по target_id, еcли такой заметки нет возвращается None"""
        target = self.str_to_int(target_id)
        if not target and target != 0:
            raise parse_exceptions.ParseIntException("Невозможно преобразовать к целому значению:", target_id)
        return self.notes.get(target)

    def get_notes_by_title(self, target_title):
        """Вернуть заметки по точному соответствию заголовка, еcли таких заметок нет возвращается пустой список []"""
        return [v for k, v in self.notes.items() if str(v.get_title()).lower() == str(target_title).lower()]

    def get_notes_by_date_time(self, datetime_begin=dt.datetime.min, datetime_end=dt.datetime.max):  # Сделать универсально через одну функцию
        """Вернуть заметки в диапазоне дат от datetime_begin (dd.mm.yyyy) до datetime_end (dd.mm.yyyy), если они опущены возврат всех заметок"""
        if datetime_begin != dt.datetime.min:
            datetime_start = datetime_begin
            datetime_begin = self.str_to_datetime(datetime_begin, Notes.datetime_format_string)
            if not datetime_begin:
                raise parse_exceptions.ParseDateTimeException(f"Невозможно преобразовать к дате в формате {Notes.datetime_format_string}: ", datetime_start)
        if datetime_end != dt.datetime.max:
            datetime_finish = datetime_end
            datetime_end = self.str_to_datetime(datetime_end, Notes.datetime_format_string)
            if not datetime_end:
                raise parse_exceptions.ParseDateTimeException(f"Невозможно преобразовать к дате в формате {Notes.datetime_format_string}: ", datetime_finish)
        return [v for k, v in self.notes.items() if (datetime_begin < v.get_datetime() < datetime_end)]

    def load_notes_csv(self, filename):
        """Загрузить все заметки из файла filename"""
        if not os.path.isfile(filename):
            f = open(filename, "w", encoding="utf-8")
            print(f"Создан файл: {filename}")
        else:
            lines_count = 0
            with open(filename, 'r', encoding="utf-8") as f:
                self.notes.clear()
                Notes.max_id = 0
                for s in f:
                    s = s.strip("\n")
                    data_parts = s.split(";")
                    datetime_to_load = self.str_to_datetime(data_parts[1], '%Y-%m-%d %H:%M:%S.%f')
                    if not datetime_to_load:
                        raise parse_exceptions.ParseDateTimeException(f"Некорректный формат файла {filename} - загрузка прервана на {lines_count} заметке: ", data_parts[1])
                    id_to_load = int(data_parts[0])
                    self.add_note(data_parts[2], data_parts[3], id_to_load, datetime_to_load)
                    lines_count += 1
            print(f"Загружено {lines_count} заметок из файла: {filename}")
        Notes.max_id = self.get_max_id()

    def save_notes_csv(self, filename):
        """Сохранить все заметки в файл filename"""
        with open(filename, "w", encoding="utf-8", newline="") as f:
            for k, v in self.notes.items():
                s = f"{k};{v.get_datetime()};{v.get_title()};{v.get_text()}\n"
                f.write(s)
        print(f"Сохранено в файл: {filename}")

    @staticmethod
    def print_notes(notes_to_print):
        """Печать всех заметок из списка notes_to_print"""
        print("******Начало заметок******")
        for el in notes_to_print:
            print(el)
        print("******Конец заметок******")

    @staticmethod
    def str_to_int(val):
        try:
            s_to_i = int(val)
            return s_to_i
        except ValueError as e:
            return None

    @staticmethod
    def str_to_datetime(val, format_string=datetime_format_string):
        try:
            s_to_dt = dt.datetime.strptime(val, format_string)
            return s_to_dt
        except ValueError as e:
            return None
