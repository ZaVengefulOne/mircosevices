import httpx
from fastapi import HTTPException
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Playlist, PlaylistTrack
from app.schemas import PlaylistCreate, PlaylistResponse, PlaylistTrackAdd
from app.database import SessionLocal
import os


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/playlist", response_model=PlaylistResponse)
def create_playlist(playlist: PlaylistCreate, user_id: str, db: Session = Depends(get_db)):
    # Проверить, существует ли пользователь
    user_service_host = os.getenv("USER_SERVICE_HOST", "user-service")
    user_service_port = os.getenv("USER_SERVICE_PORT", "5001")
    user_service_url = f"http://{user_service_host}:8000/api/user"
    try:
        response = httpx.get(f"{user_service_url}/check?user_id={user_id}")
        response.raise_for_status()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=400, detail="User service returned an error")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error contacting user service: {exc}")

    # Создать плейлист
    new_playlist = Playlist(name=playlist.name)
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return PlaylistResponse(id=new_playlist.id, name=new_playlist.name)

@router.post("/playlist/track", response_model=dict)
def add_track_to_playlist(track: PlaylistTrackAdd, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == track.playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    new_track = PlaylistTrack(playlist_id=track.playlist_id, track_id=track.track_id)
    db.add(new_track)
    db.commit()
    return {"result": True}

@router.delete("/playlist/{playlist_id}", response_model=dict)
def delete_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    db.delete(playlist)
    db.commit()
    return {"result": True}

@router.delete("/api/playlist/{playlist_id}/track/{track_id}", response_model=dict)
def delete_track_from_playlist(playlist_id: str, track_id: str, db: Session = Depends(get_db)):
    track = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found in the specified playlist")
    db.delete(track)
    db.commit()
    return {"result": True}
