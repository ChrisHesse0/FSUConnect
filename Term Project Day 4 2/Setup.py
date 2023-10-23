import sqlite3

#Create database with Tables: Login, Comments, Likes, Messages
print("TEST")
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT, First TEXT, Last TEXT, Description TEXT, Major TEXT, GPA TEXT, GradYear INTEGER, Gender TEXT, FSUID TEXT, Status TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Comments (FSUID TEXT, Commenter TEXT, Comment TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Likes (LikeTo TEXT, LikeFrom TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Messages (SentFrom TEXT, SentTo TEXT, Message TEXT, Ind TEXT)')

cursor.close()


