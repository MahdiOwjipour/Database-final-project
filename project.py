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

    def connect_db(self):
        self.connect = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )

    def execute_query(self, query, data=None, fetch=False):
        self.connect_db()
        try:
            cursor = self.connect.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            if fetch:
                result = cursor.fetchall()
                return result
            self.connect.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            self.connect.close()

    def create_tables(self):
        create_image_table = """
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
        create_article_table = """
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
        self.execute_query(create_image_table)
        self.execute_query(create_article_table)

    def insert_image(self, image):
        query = """
        INSERT INTO Images (image_path, title, tags, description, category, photographer_code, photographer_name, photographer_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (
            image.image_path, image.title, image.tags, image.description,
            image.category, image.photographer_code, image.photographer_name, image.photographer_email
        )
        self.execute_query(query, data)

    def insert_article(self, article):
        query = """
        INSERT INTO Articles (content, keywords, title, category, writer_code, writer_name, writer_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        data = (
            article.content, article.keywords, article.title, article.category,
            article.writer_code, article.writer_name, article.writer_email
        )
        self.execute_query(query, data)

    def update_image(self, image_id, image_path=None, title=None, tags=None, description=None, category=None, photographer_code=None, photographer_name=None, photographer_email=None):
        updates = []
        data = []
        if image_path:
            updates.append("image_path = %s")
            data.append(image_path)
        if title:
            updates.append("title = %s")
            data.append(title)
        if tags:
            updates.append("tags = %s")
            data.append(tags)
        if description:
            updates.append("description = %s")
            data.append(description)
        if category:
            updates.append("category = %s")
            data.append(category)
        if photographer_code:
            updates.append("photographer_code = %s")
            data.append(photographer_code)
        if photographer_name:
            updates.append("photographer_name = %s")
            data.append(photographer_name)
        if photographer_email:
            updates.append("photographer_email = %s")
            data.append(photographer_email)
        
        query = "UPDATE Images SET " + ", ".join(updates) + " WHERE image_id = %s"
        data.append(image_id)
        self.execute_query(query, data)
        print(f"Image with ID {image_id} updated")

    def update_article(self, article_id, content=None, keywords=None, title=None, category=None, writer_code=None, writer_name=None, writer_email=None):
        updates = []
        data = []
        if content:
            updates.append("content = %s")
            data.append(content)
        if keywords:
            updates.append("keywords = %s")
            data.append(keywords)
        if title:
            updates.append("title = %s")
            data.append(title)
        if category:
            updates.append("category = %s")
            data.append(category)
        if writer_code:
            updates.append("writer_code = %s")
            data.append(writer_code)
        if writer_name:
            updates.append("writer_name = %s")
            data.append(writer_name)
        if writer_email:
            updates.append("writer_email = %s")
            data.append(writer_email)
        
        query = "UPDATE Articles SET " + ", ".join(updates) + " WHERE article_id = %s"
        data.append(article_id)
        self.execute_query(query, data)
        print(f"Article with ID {article_id} updated")

    def delete_image(self, image_id):
        query = "DELETE FROM Images WHERE image_id = %s"
        self.execute_query(query, (image_id,))
        print(f"Image with ID {image_id} deleted")

    def delete_article(self, article_id):
        query = "DELETE FROM Articles WHERE article_id = %s"
        self.execute_query(query, (article_id,))
        print(f"Article with ID {article_id} deleted")
        
    def fetch_images(self):
        query = "SELECT * FROM Images"
        result = self.execute_query(query, fetch=True)
        for row in result:
            print(row)
        return result

    def fetch_articles(self):
        query = "SELECT * FROM Articles"
        result = self.execute_query(query, fetch=True)
        for row in result:
            print(row)
        return result

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

if __name__ == "__main__":
    db = DB(user="your_user", password="your_password", host="your_host", database="your_database")
    db.create_tables()
    read_csv_and_insert_images(db, 'path_to_images_csv.csv')
    read_csv_and_insert_articles(db, 'path_to_articles_csv.csv')
