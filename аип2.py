print("Задание 1")

dict_1 = {1: 'a', 2: 'b'}
dict_2 = {2: 'c', 4: 'd'}

dict_3 = dict_1 | dict_2
dict_4 = dict_1.copy()
dict_4.update(dict_2)

print("Результат с использованием оператора |:", dict_3)
print("Результат с использованием метода update():", dict_4)



print("\nЗадание 2")

def max_dict(*dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result:
                result[key] = max(result[key], value)
            else:
                result[key] = value
    return result

def sum_dict(*dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value
    return result

dict_1 = {1: 12, 2: 33, 3: 10, 4: 10, 5: 2, 6: 90}
dict_2 = {1: 12, 3: 7, 4: 1, 5: 2, 7: 112}
dict_3 = {2: 3, 3: 3, 4: 60, 6: 8, 7: 25, 8: 71}
dict_4 = {3: 1, 4: 13, 5: 31, 9: 9, 10: 556}

print(max_dict(dict_1, dict_2))
print(sum_dict(dict_1, dict_4, dict_3))
print(max_dict(dict_1, dict_2, dict_3, dict_4))
print(sum_dict(dict_1, dict_2, dict_3, dict_4))



print("\nЗадание 3")

def set_gen(numbers):
    count = {}
    result_set = set()
    
    for number in numbers:
        if number in count:
            count[number] += 1
            result_set.add(str(number) * count[number])
        else:
            count[number] = 1
            result_set.add(number)
            
    return result_set

list_1 = [1, 1, 3, 3, 1]
list_2 = [5, 5, 5, 5, 5, 5, 5]
list_3 = [2, 2, 1, 2, 2, 5, 6, 7, 1, 3, 2, 2]

print(set_gen(list_1))  # {1, 3, '111', '33', '11'}
print(set_gen(list_2))  # {'5555555', 5, '55', '55555', '5555', '555555', '555'}
print(set_gen(list_3))  # {1, 2, 3, 5, 6, 7, '22', '2224', '22222', '222', '11', '222222'}



print("\nЗадание 4")

def superset(set_a, set_b):
    if set_a == set_b:
        print("Множества равны")
    elif set_a > set_b:
        print(f"Объект {set_a} является чистым супермножеством")
    elif set_b > set_a:
        print(f"Объект {set_b} является чистым супермножеством")
    else:
        print("Супермножество не обнаружено")

set_1 = {1, 8, 3, 5}
set_2 = {3, 5}
set_3 = {5, 3, 8, 1}
set_4 = {90, 100}

superset(set_1, set_2)  # Объект {8, 1, 3, 5} является чистым супермножеством
superset(set_1, set_3)  # Множества равны
superset(set_2, set_3)  # Объект {8, 1, 3, 5} является чистым супермножеством
superset(set_4, set_2)  # Супермножество не обнаружено
