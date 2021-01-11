import mysql.connector as db

def migrate():
    try:
        mydb = db.connect(
            host='localhost',
            user='root',
            passwd='xCaliber73',
            database='scraping_final',
            auth_plugin='mysql_native_password'
        )
        print('Database up and running!')
    except Exception as err:
        print('No such database, creating new one...')
        try:
            mydb = db.connect(
                host='localhost',
                user='root',
                passwd='xCaliber73',
                auth_plugin='mysql_native_password'
            )
            mycursor = mydb.cursor()
            mycursor.execute("CREATE DATABASE scraping_final")  
            print('Created new database: scraping_final')
            mydb = db.connect(
                host='localhost',
                user='root',
                passwd='xCaliber73',
                database='scraping_final',
                auth_plugin='mysql_native_password'
            )
            mycursor = mydb.cursor()
            mycursor.execute("SHOW TABLES")
            if 'posts' in mycursor:
                print('posts table exists!')
            else:
                print('posts table not found. creating...')
                mycursor.execute("CREATE TABLE posts (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author_name VARCHAR(255), content TEXT, post_time VARCHAR(255))")
                print('Created posts table!')
        except Exception as err:
            print(err)

def reduce_duplicates(new_posts):
    try:
        mydb = db.connect(
            host='localhost',
            user='root',
            passwd='xCaliber73',
            database='scraping_final',
            auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT title,author_name,content,post_time FROM posts")
        db_posts = mycursor.fetchall()
        if len(db_posts) > 0:
            filtered_posts = []
            for post in new_posts:
                current_post_title = post[0]
                exists = False
                for db_post in db_posts:
                    if db_post[0] == current_post_title:
                        exists = True
                if not exists:
                    filtered_posts.append(post)
            print(f"Filtered posts count ==> {len(filtered_posts)}")
            return filtered_posts
        else: return new_posts
    except Exception as err:
        print(err)
def insert_data(data):
    mydb = db.connect(
        host='localhost',
        user='root',
        passwd='xCaliber73',
        database='scraping_final',
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO posts (title, author_name, content, post_time) VALUES (%s, %s, %s, %s)"
    val = data
    mycursor.executemany(sql, val)
    mydb.commit()
    msg = f"{mycursor.rowcount}, record inserted."
    return msg