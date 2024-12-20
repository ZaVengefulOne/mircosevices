from pydantic import BaseModel

class PlaylistCreate(BaseModel):
    name: str

class PlaylistResponse(BaseModel):
    id: str
    name: str

class PlaylistTrackAdd(BaseModel):
    playlist_id: str
    track_id: str
