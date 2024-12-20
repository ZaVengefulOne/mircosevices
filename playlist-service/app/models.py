from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    playlist_id = Column(String, ForeignKey("playlists.id"), nullable=False)
    track_id = Column(String, nullable=False)
    playlist = relationship("Playlist", back_populates="tracks")

Playlist.tracks = relationship("PlaylistTrack", back_populates="playlist")
