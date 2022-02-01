import xlrd, copy
from typing import Any
from lxml import etree as ET


def _get_data_book(file) -> list:
    book = xlrd.open_workbook(file_contents=file)
    sheet = book.sheets()[0]
    data = [sheet.row_values(i) for i in range(sheet.nrows) if not sheet.row_values(i)[2] == ""]
    return data


def _get_tag(var):
    if var.isalnum():
        return 'True'
    else:
        return 'False'


class Picklist:
    alfavit = {1: [i for i in "АБВабв"],
               2: [i for i in "ГДЕЁЖгдеёж"],
               3: [i for i in "ЗИКзик"],
               4: [i for i in "ЛМНОлмно"],
               5: [i for i in "ПРСТУпрсту"],
               6: [i for i in "ФХЦЧШфхцчш"],
               8: [i for i in "ЩЪЫЬЭЮЯщъыьэюя"]}
    tmp_xls = r'.\static\template.xml'
    tree = ET.parse(tmp_xls)

    def __init__(self):
        self.root = self.tree.getroot()
        self.items = self.root.find("Items")
        self.new_item = self.root.find(".//Item")

    def _get_category(self, name):
        if str(name)[0].isalpha():
            for i in self.alfavit:
                if str(name)[0] in self.alfavit[i]:
                    return str(i)
            print('Warning! Наименование "%s" начинается не на букву киррилицы' % name)
        else:
            print('Warning! Наименование "%s" начинается не на букву' % name)
            return '1'

    def _edit_list(self, upc, name, cat, vis, pop, quick) -> None:
        vis = _get_tag(vis)
        pop = _get_tag(pop)
        quick = _get_tag(quick)
        if self.items.xpath("./*[@UPC=$upc]", upc=upc):  # Проверка на наличие ТП в листе
            item = self.items.xpath("./*[@UPC=$upc]", upc=upc)[0]
            for i in item.findall("./Languages//*Description"):
                if not i.text == name:
                    i.text = name
            for i in item.findall("./Languages//*Categories"):
                if not i.text == cat:
                    i.text = cat
            if not item.find("./IsQuickPickItem").text == quick:
                item.find("./IsQuickPickItem").text = quick
            if vis == 'True':
                item.find("./IsVisible").text = vis
        else:  # ТП с ШК еще нет в листе, добавляем новый
            # print('Info. Добавление новой ТП %s "%s"' % (upc, name))
            item = copy.copy(self.new_item)
            item.set("UPC", upc)
            for i in item.findall("./Languages//*Description"):
                i.text = name
            for i in item.findall("./Languages//*Categories"):
                i.text = cat
            item.find("./IsPopular").text = pop
            item.find("./IsVisible").text = vis
            item.find("./IsQuickPickItem").text = quick
            self.items.append(item)

    def _get_picklist(self, xls) -> Any:
        for tp in xls[1:]:
            if len(tp) >= 2:
                if str(tp[0]).split('.')[0].isdigit():  # Проверка ШК на отсутствие букв, только цифры.
                    # Определяем категорию по наименованию товара
                    cat = self._get_category(tp[1])
                    # Добавляем товары в xml
                    self._edit_list(str(tp[0]).split('.')[0], tp[1].strip(), cat, str(tp[2]), str(tp[3]), str(tp[4]))
                else:
                    print('Warning! ШК %s не корректен' % tp[0])
        count_upc = len(self.items.getchildren())
        self.root.find("Parameters/PickListSize").text = str(count_upc)  # Задаем размер пиклиста (кол-во ТП)
        self.tree = ET.ElementTree(self.root)
        # tree.write(file_pl, encoding='UTF-16', xml_declaration=True)

        return ET.tostring(self.root)

    def converter(self, file):
        data_xls = _get_data_book(file)
        self._get_picklist(data_xls)
        return ET.tostring(self.root, encoding='UTF-8', xml_declaration=True)
