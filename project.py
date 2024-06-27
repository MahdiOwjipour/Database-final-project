import mysql.connector
import csv

class Image:
    def __init__(self, image_path, title, tags, description, category, photographer_code, photographer_name, photographer_email):
        self.image_path = image_path
        self.title = title
        self.tags = tags
        self.description = description
        self.category = category
        self.photographer_code = photographer_code
        self.photographer_name = photographer_name
        self.photographer_email = photographer_email

class Article:
    def __init__(self, content, keywords, title, category, writer_code, writer_name, writer_email):
        self.content = content
        self.keywords = keywords
        self.title = title
        self.category = category
        self.writer_code = writer_code
        self.writer_name = writer_name
        self.writer_email = writer_email

class DB:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connect = None

    def connection(self):
        self.connect = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    def execute_query(self, query, data=None, fetch=False):
        self.connection()
        try:
            mycursor = self.connect.cursor()
            if data:
                mycursor.execute(query, data)
            else:
                mycursor.execute(query)
            if fetch:
                result = mycursor.fetchall()
                return result
            self.connect.commit()
            print("DONE!")
        except Exception as e:
            print(e)
        finally:
            mycursor.close()
            self.connect.close()

    def create_tables(self):
        image_table_query = """
        CREATE TABLE IF NOT EXISTS Images (
            image_id INT AUTO_INCREMENT PRIMARY KEY,
            image_path VARCHAR(255),
            title VARCHAR(255),
            tags TEXT,
            description TEXT,
            category VARCHAR(255),
            photographer_code VARCHAR(255),
            photographer_name VARCHAR(255),
            photographer_email VARCHAR(255)
        );
        """
        article_table_query = """
        CREATE TABLE IF NOT EXISTS Articles (
            article_id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT,
            keywords TEXT,
            title VARCHAR(255),
            category VARCHAR(255),
            writer_code VARCHAR(255),
            writer_name VARCHAR(255),
            writer_email VARCHAR(255)
        );
        """
        self.execute_query(image_table_query)
        self.execute_query(article_table_query)

    def insert_image(self, image):
        query = """
        INSERT INTO Images (image_path, title, tags, description, category, photographer_code, photographer_name, photographer_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (image.image_path, image.title, image.tags, image.description, image.category, image.photographer_code, image.photographer_name, image.photographer_email)
        self.execute_query(query, data)

    def insert_article(self, article):
        query = """
        INSERT INTO Articles (content, keywords, title, category, writer_code, writer_name, writer_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        data = (article.content, article.keywords, article.title, article.category, article.writer_code, article.writer_name, article.writer_email)
        self.execute_query(query, data)

def read_csv_and_insert_images(db, file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image = Image(
                row['image_path'], row['title'], row['tags'], row['description'],
                row['category'], row['photographer_code'], row['photographer_name'], row['photographer_email']
            )
            db.insert_image(image)

def read_csv_and_insert_articles(db, file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            article = Article(
                row['content'], row['keywords'], row['title'], row['category'],
                row['writer_code'], row['writer_name'], row['writer_email']
            )
            db.insert_article(article)

# Example usage:
if __name__ == "__main__":
    db = DB(user="your_user", password="your_password", host="your_host", database="your_database")
    db.create_tables()
    read_csv_and_insert_images(db, 'path_to_images_csv.csv')
    read_csv_and_insert_articles(db, 'path_to_articles_csv.csv')
