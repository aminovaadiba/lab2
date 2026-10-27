import csv
import random
import xml.etree.ElementTree as ET


file_books = open("books.csv", encoding="utf-8-sig")
reader = csv.reader(file_books, delimiter=";")
all_rows = list(reader)  
file_books.close()

books = all_rows[1:]  
COL_TITLE = 1    
COL_AUTHOR = 3  
COL_DATE = 6    
COL_ISSUED = 8   
COL_GENRE = 12   

YEAR_LIMIT = 2016 


def get_year(book):
    date_part = book[COL_DATE].split(" ")[0]  
    year = date_part.split(".")[-1]  
    return int(year)


print("Задание №1")

count_long = 0  

for book in books:
    title = book[COL_TITLE]
    if len(title) > 30:
        count_long += 1

print("Записей с названием длиннее 30 символов:", count_long)
print()

print("Задание №2")


def search_by_author(query, max_year): 
    found = []
    for book in books:
        author = book[COL_AUTHOR]
        year = get_year(book)
        if query.lower() in author.lower() and year < max_year:
            found.append(book)  
    return found


user_author = input("Введите автора: ")
result = search_by_author(user_author, YEAR_LIMIT)
print("Найдено записей:", len(result))

for book in result:
    print("-", book[COL_AUTHOR], "|", book[COL_TITLE], "| год:", get_year(book))
print()

print("Задание №3")


def make_reference(book):
    author = book[COL_AUTHOR]
    title = book[COL_TITLE]
    year = get_year(book)
    return author + ". " + title + " - " + str(year)


books_with_author = []
for book in books:
    if book[COL_AUTHOR] != "":
        books_with_author.append(book)

chosen = random.sample(books_with_author, 20)  
out_file = open("references.txt", "w", encoding="utf-8")
number = 1  # номер строки
for book in chosen:
    reference = make_reference(book)
    line = str(number) + ". " + reference  
    out_file.write(line + "\n")
    print(line)
    number += 1

out_file.close()
print("Список сохранён в файл references.txt")
print()

print("Задание №4")

tree = ET.parse("currency.xml")  
root = tree.getroot() 
names = []
values = []

for valute in root.findall("Valute"):  
    name_text = valute.find("Name").text
    value_text = valute.find("Value").text
    names.append(name_text)
    values.append(float(value_text.replace(",", ".")))  

print("Name :", names)
print("Value:", values)
print()

print("Допзадание №1: все теги без повторений")

tags = set()  
for book in books:
    for tag in book[COL_GENRE].split("#"):  
        tag = tag.strip()  
        if tag != "":
            tags.add(tag)

print("Уникальных тегов:", len(tags))
print(sorted(tags))
print()

print("Допзадание №2: 20 самых популярных книг")


issued_by_book = {}
for book in books:
    key = book[COL_AUTHOR] + ". " + book[COL_TITLE]
    if key not in issued_by_book:
        issued_by_book[key] = 0
    issued_by_book[key] += int(book[COL_ISSUED])

top = sorted(issued_by_book.items(), key=lambda item: item[1], reverse=True)[:20]
number = 1
for key, issued in top:
    print(str(number) + ".", key, "-", issued, "выдач")
    number += 1