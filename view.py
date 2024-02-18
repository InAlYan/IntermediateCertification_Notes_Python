import parse_exceptions


class View:

    def __init__(self, model, filename):
        self.model = model
        self.filename = filename

    def run(self):

        try:
            self.model.load_notes_csv(self.filename)
        except parse_exceptions.ParseDateTimeException as e:
            print(e)

        command = ""
        while command != "q":

            command = input("Команда: a-добавить, e-редактировать, d-удалить, p-печатать, pd-печатать по диапазону "
                            "дат, f-найти по номеру, ft-найти по заголовку, q-выход: \n")

            if command == "p":
                self.model.print_notes(self.model.get_notes_by_date_time())

            if command == "pd":
                try:
                    print("Отбор заметок в диапазоне от даты начала приведенной к 00ч 00мин 00сек по дату окончания приведенной к 00ч 00мин 00сек")
                    self.model.print_notes(self.model.get_notes_by_date_time(input("Начальная дата диапазона в формате " + self.model.datetime_format_string + ": "),
                                                                             input("Конечная дата диапазона в формате " + self.model.datetime_format_string + ": ")))
                except parse_exceptions.ParseDateTimeException as e:
                    print(e)

            if command == "f":
                try:
                    print(self.model.get_note_by_id(input("Найти заметку по номеру: ")))
                except parse_exceptions.ParseIntException as e:
                    print(e)

            if command == "ft":
                self.model.print_notes(self.model.get_notes_by_title(input("Введите заголовок заметки для поиска: ")))

            if command == "a":
                print("Добавлена: " + f"{self.model.get_note_by_id(self.model.add_note(input('Введите заголовок заметки: '), input('Введите текст заметки: ')))}")

            if command == "e":
                try:
                    res = self.model.get_note_by_id(input("Введите идентификатор существующей заметки для редактирования: "))
                    if res:
                        res = self.model.edit_note(res.get_id(), input("Введите новый заголовок заметки: "), input("Введите новый текст заметки: "))
                    print("Отредактирована: " + f"{res}")
                except parse_exceptions.ParseIntException as e:
                    print(e)

            if command == "d":
                try:
                    print("Удалена: " + f"{self.model.delete_note(input('Введите идентификатор существующей заметки для удаления: '))}")
                except parse_exceptions.ParseIntException as e:
                    print(e)

        self.model.save_notes_csv(self.filename)



