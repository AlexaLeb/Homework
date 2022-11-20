# Задача 1
def open_file(file):
    file_data = open(file, "r")
    data = file_data.read()
    splited = data.split("\n")
    return splited


def split_on(what, delimiter=''):
    splitted = [[]]
    for item in what:
        if item == delimiter:
            splitted.append([])
        else:
            splitted[-1].append(item)
    splitted_full = list(filter(None, splitted))
    return splitted_full


def dict_create(info):
    name = {

    }
    for recepi in info:
        heading = recepi[0]
        values = []
        for part_recepi in recepi[2:]:
            part = part_recepi.split(' | ')
            sub_dict = {
                'ingredient_name': part[0],
                'quantity': part[1],
                'measure': part[2]
            }
            values.append(sub_dict)
        name[heading] = values
    return name


riading_form = open_file("Home work/Список продуктов.rtf")
cook_list = split_on(riading_form)
cook_book = dict_create(cook_list)
# Решение задачи 1
print(cook_book)

# Задача 2

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {

    }
    for dish in dishes:
        for name, recipe in cook_book.items():
            if name == dish:
                for ingredient, val, measure in recipe:
                    val = val * person_count
                    shop_list[ingredient] = [measure, val]
    return shop_list

task_two = (get_shop_list_by_dishes(["Омлет", "Запеченный картофель"], 3))
print(task_two)



