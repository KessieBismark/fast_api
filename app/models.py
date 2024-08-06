# from sqlalchemy.testing.schema import Column, Integer,String
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from .dbconfig import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # setting up a foreign key
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('post_id', 'user_id', name='votes_pk'),
    )
    # this is for composite key which is a primary key that spans on multiple columns
    # Optionally, you can define relationships if needed
    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")
