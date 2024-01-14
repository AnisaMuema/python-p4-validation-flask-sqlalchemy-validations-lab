from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validates_authors(self, key, name):
        if not name:
            raise ValueError('Author must have a name')
    
        author_duplicate = self.query.filter(Author.name == name).first()
        if author_duplicate is not None:
            raise ValueError("Duplicate name found")

        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            if not phone_number.isdigit() or len(phone_number) !=10:
                raise ValueError("Author phone number must be exactly ten digits and contain only digits")
            
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
            

    # Add validators 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def validates_post_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be atleast 250 characters long")
        return content
    
    @validates('summary')
    def validates_post_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summery must be 250 characters long")
        return summary
    
    @validates('category')
    def validates_post_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category should be in either 'Fiction' or 'Non-Fiction")
        return category
    
    @validates('title')
    def validates_post_title(self, key, title):
        click_bait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in click_bait_words):
            raise ValueError("Post title must be suffiently clickbait-y")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
