import sqlite3
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

genres = [
    'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Thriller', 'Horror',
    'Historical', 'Adventure', 'Non-Fiction', 'Biography', 'Self-Help',
    'Drama', 'Poetry', 'Classic', 'Graphic Novel', 'Young Adult'
]

def random_publish_date(birth_date):
    birth_date = datetime.strptime(str(birth_date), '%Y-%m-%d')
    birth_date = birth_date + timedelta(days=10 * 365)
    end_date = datetime.today()
    publish_date = randint(0, (end_date - birth_date).days)
    return (birth_date + timedelta(days=publish_date)).strftime('%Y-%m-%d')


fake = Faker('en_US')

cursor.execute(""" CREATE TABLE IF NOT EXISTS author(
               ID INTEGER PRIMARY KEY,
               first_name TEXT,
               last_name TEXT,
               birth_date TEXT,
               birth_address TEXT
               ) """)


cursor.execute(""" CREATE TABLE IF NOT EXISTS book(
               ID INTEGER PRIMARY KEY,
               title TEXT,
               genre TEXT,
               pages INTEGER,
               publish_date TEXT,
               author_ID INTEGER,
               FOREIGN KEY (author_ID) REFERENCES author (ID)
               ) """)


author_id_and_birth_date = []
for _ in range(500):
    name = fake.first_name()
    surname = fake.last_name()
    birth_date = fake.date_of_birth(minimum_age=10, maximum_age=70)
    birth_address = fake.address()
    cursor.execute("INSERT INTO author(first_name, last_name, birth_date, birth_address) VALUES (?, ?, ?, ?)", (name, surname, birth_date, birth_address))
    author_id_and_birth_date.append((cursor.lastrowid, birth_date))


for _ in range(1000):
    title = fake.sentence(nb_words=4)
    genre = choice(genres)
    pages = randint(25, 1200)
    author_id, author_birth_date = choice(author_id_and_birth_date)
    publish_date = random_publish_date(author_birth_date)
    cursor.execute("INSERT INTO book(title, genre, pages, publish_date, author_ID) VALUES (?, ?, ?, ?, ?)",
                   (title, genre, pages, publish_date, author_id))

conn.commit()



#იპოვეთ და დაბეჭდეთ ყველაზე მეტი გვერდების მქონე წიგნის ყველა ველი

cursor.execute("SELECT * FROM book WHERE pages = (SELECT MAX(pages) FROM book)")
book_with_max_pages = cursor.fetchall()
for book in book_with_max_pages:
    print(f"Here is all the information about book with maximum number of pages:\n\
ID: {book[0]}\n\
Title: {book[1]}\n\
Genre: {book[2]}\n\
Pages: {book[3]}\n\
Publish Date: {book[4]}\n\
Author ID: {book[5]}")

#იპოვეთ და დაბეჭდეთ წიგნების საშუალო გვერდების რაოდენობა

cursor.execute("SELECT AVG(pages) FROM book")
book_avg_pages = cursor.fetchall()
for i in book_avg_pages:
    avg_pages = round(i[0])
    print(f"The average number of pages in books is {avg_pages}.")

#დაბეჭდეთ ყველაზე ახალგაზრდა ავტორი

cursor.execute("SELECT first_name, last_name, birth_date FROM author WHERE birth_date = (SELECT MIN(birth_date) FROM author)")
youngest_author = cursor.fetchall()
for author in youngest_author:
    print(f"The youngest author is {author[0]} {author[1]} who was born in {author[2]}.")

#დაბეჭდეთ ისეთი ავტორები რომელსაც ჯერ წიგნი არ აქვს

cursor.execute("""SELECT author.first_name, author.last_name 
               FROM author
               LEFT JOIN book ON author.ID = book.author_ID
               WHERE book.author_ID IS NULL""")

authors_with_no_books = cursor.fetchall()
print("Authors with no books are: ")
for author in authors_with_no_books:
    print(f"{author[0]} {author[1]}")

# ბონუს დავალება:
# იპოვეთ ისეთი 5 ავტორი რომელსაც 3 ზე მეტი წიგნი აქვს

cursor.execute("""SELECT author.first_name, author.last_name
               FROM author
               LEFT JOIN book ON author.ID = book.author_ID
               GROUP BY author.id, author.first_name, author.last_name
               HAVING COUNT(book.author_ID) > 3
               LIMIT 5""")

five_authors = cursor.fetchall()
print('5 Authors with more than 3 books are: ')
for author in five_authors:
    print(f"{author[0]} {author[1]}")

conn.close()
