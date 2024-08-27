import enum
from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class AccountType(enum.Enum):
    PERSONAL = "personal"
    CREATOR = "creator"
    BUSINESS = "business"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    facebook_id = Column(Integer)
    threads_id = Column(Integer)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    profile_photo_id = Column(Integer, ForeignKey("media.id"))
    former_usernames_count = Column(Integer, nullable=False, default=1)
    account_type = Column(Enum(AccountType), nullable=False)
    is_private = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Follow(Base):
    __tablename__ = "follow"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_closed_friend = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

# Based on the following links:
# https://softwareengineering.stackexchange.com/questions/357900/whats-a-universal-way-to-store-a-geographical-address-location-in-a-database
# https://developer.android.com/reference/android/location/Address
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    address_line = Column(String)
    admin_area = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    feature_name = Column(String)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)    
    # I am assuming music is fetched from Spotify API
    music_url = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"))
    is_reel = Column(Boolean, nullable=False, default=False)
    is_ad = Column(Boolean, nullable=False, default=False)
    ad_redirect_url = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class MediaType(enum.Enum):
    IMAGE = "image"
    GIF = "gif"
    VIDEO = "video"

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    type = Column(Enum(MediaType), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    tagged_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class PostMedia(Base):
    __tablename__ = "post_media"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    index_in_post = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class PostLike(Base):
    __tablename__ = "post_like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Save(Base):
    __tablename__ = "save"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    replied_comment_id = Column(Integer, ForeignKey("comment.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class CommentLike(Base):
    __tablename__ = "comment_like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comment.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Highlight(Base):
    __tablename__ = "highlight"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    index_in_profile = Column(Integer, nullable=False, default=0)
    name = Column(String, nullable=False)
    cover_photo_id = Column(Integer, ForeignKey("media.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class HighlightStory(Base):
    __tablename__ = "highlight_story"
    id = Column(Integer, primary_key=True)
    highlight_id = Column(Integer, ForeignKey("highlight.id"), nullable=False)
    story_id = Column(Integer, ForeignKey("story.id"), nullable=False)
    index_in_highlight = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cover_photo_id = Column(Integer, ForeignKey("media.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class ChatMember(Base):
    __tablename__ = "chat_member"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    text = Column(String)
    media_id = Column(Integer, ForeignKey("media.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class MessageLike(Base):
    __tablename__ = "message_like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("message.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Seen(Base):
    __tablename__ = "seen"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("message.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

# Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
