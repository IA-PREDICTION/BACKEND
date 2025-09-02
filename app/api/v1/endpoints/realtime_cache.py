from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.db.session import get_db
from app.models.cache_entry import CacheEntry
from app.models.queue_job import QueueJob, JobStatus
from app.models.websocket_connection import WebsocketConnection
from app.core.deps import get_current_user  
import uuid
import json

router = APIRouter()

# ---------- WebSocket ----------
@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, room: Optional[str] = Query(None), db: Session = Depends(get_db)):
    await websocket.accept()
    conn_id = str(uuid.uuid4())
    ip = websocket.client.host if websocket.client else None
    rooms = [room] if room else []

    ws = WebsocketConnection(connection_id=conn_id, ip_address=ip, rooms=rooms, connected_at=datetime.utcnow())
    db.add(ws)
    db.commit()

    try:
        await websocket.send_text(json.dumps({"event": "connected", "connection_id": conn_id, "rooms": rooms}))
        while True:
            msg = await websocket.receive_text()
            # On traite un "ping"
            ws.last_ping = datetime.utcnow()
            db.add(ws)
            db.commit()
            await websocket.send_text(json.dumps({"event": "pong", "at": datetime.utcnow().isoformat()}))
    except WebSocketDisconnect:
        # On supprime l'entrée à la déconnexion
        db.delete(ws)
        db.commit()

# ---------- Cache ----------
@router.get("/cache/{key}")
def cache_get(key: str, db: Session = Depends(get_db)):
    row = db.query(CacheEntry).filter(CacheEntry.cache_key == key).first()
    if not row:
        raise HTTPException(status_code=404, detail="Key not found")
    if row.expire_at and row.expire_at < datetime.utcnow():
        # expired -> delete
        db.delete(row); db.commit()
        raise HTTPException(status_code=404, detail="Key expired")
    return {"key": key, "value": row.cache_value, "expire_at": row.expire_at}

@router.post("/cache/{key}")
def cache_set(key: str, value: str, ttl_seconds: int = 300, tags: Optional[dict] = None, db: Session = Depends(get_db)):
    expire_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    row = db.query(CacheEntry).filter(CacheEntry.cache_key == key).first()
    if row:
        row.cache_value = value
        row.ttl_seconds = ttl_seconds
        row.expire_at = expire_at
        row.tags = tags
    else:
        row = CacheEntry(cache_key=key, cache_value=value, ttl_seconds=ttl_seconds, expire_at=expire_at, tags=tags)
        db.add(row)
    db.commit()
    return {"ok": True, "key": key, "expire_at": expire_at}

@router.delete("/cache/{key}")
def cache_del(key: str, db: Session = Depends(get_db)):
    cnt = db.query(CacheEntry).filter(CacheEntry.cache_key == key).delete()
    db.commit()
    return {"deleted": cnt}

# ---------- Queue (mini-API fiable pour tests) ----------
@router.post("/queue/enqueue")
def enqueue(queue_name: str, job_type: str, payload: dict, scheduled_in_seconds: int = 0, priorite: int = 0, db: Session = Depends(get_db)):
    scheduled_at = datetime.utcnow() + timedelta(seconds=scheduled_in_seconds) if scheduled_in_seconds > 0 else None
    job = QueueJob(
        queue_name=queue_name,
        job_type=job_type,
        payload=payload,
        statut=JobStatus.en_attente,
        priorite=priorite,
        scheduled_at=scheduled_at
    )
    db.add(job); db.commit(); db.refresh(job)
    return {"id": job.id, "statut": job.statut}

@router.post("/queue/poll")
def poll(queue_name: str, db: Session = Depends(get_db)):
    # récupère le job prêt le plus prioritaire
    now = datetime.utcnow()
    job = (
        db.query(QueueJob)
        .filter(
            QueueJob.queue_name == queue_name,
            QueueJob.statut == JobStatus.en_attente,
            sa.or_(QueueJob.scheduled_at == None, QueueJob.scheduled_at <= now)
        )
        .order_by(QueueJob.priorite.desc(), QueueJob.id.asc())
        .with_for_update(skip_locked=True)  # verrouillage optimiste (si PG >= 9.5)
        .first()
    )
    if not job:
        return {"job": None}
    job.statut = JobStatus.en_cours
    job.started_at = now
    db.commit(); db.refresh(job)
    return {"job": {"id": job.id, "type": job.job_type, "payload": job.payload}}

@router.post("/queue/complete")
def complete(job_id: int, db: Session = Depends(get_db)):
    job = db.query(QueueJob).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    job.statut = JobStatus.complete
    job.completed_at = datetime.utcnow()
    db.commit()
    return {"ok": True}

@router.post("/queue/fail")
def fail(job_id: int, error_message: str = "", db: Session = Depends(get_db)):
    job = db.query(QueueJob).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    job.tentatives += 1
    job.statut = JobStatus.echoue
    job.error_message = error_message
    db.commit()
    return {"ok": True, "tentatives": job.tentatives}
