from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, WebSocketDisconnect

app = FastAPI()

# Serve downloaded files
app.mount("/files", StaticFiles(directory=DOWNLOAD_DIR), name="files")

# In-memory set of connected WebSocket clients
websocket_clients = set()

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        websocket_clients.remove(websocket)

async def broadcast_notification(message: str):
    to_remove = set()
    for ws in websocket_clients:
        try:
            await ws.send_text(message)
        except Exception:
            to_remove.add(ws)
    for ws in to_remove:
        websocket_clients.remove(ws)

# Modify scrape_and_store_tenders to broadcast new tenders
import asyncio

def scrape_and_store_tenders():
    db = SessionLocal()
    tenders = eprocure.fetch_tenders()
    for tender in tenders:
        if db.query(Tender).filter(Tender.url == tender["url"]).first():
            continue
        category = categorize_tender(tender)
        files = eprocure.download_documents(tender["url"], DOWNLOAD_DIR)
        doc_path = files[0] if files else None
        if doc_path and doc_path.endswith(".pdf"):
            pdf_text = extract_text_from_pdf(doc_path)
            tender["description"] += "\n" + pdf_text[:1000]  # Append first 1000 chars
        t = Tender(
            title=tender["title"],
            url=tender["url"],
            category=category,
            description=tender["description"],
            document_path=doc_path
        )
        db.add(t)
        db.commit()
        if EMAIL_NOTIFICATIONS:
            send_email_notification(
                f"New Tender: {t.title}",
                f"Category: {t.category}\nURL: {t.url}\nDescription: {t.description[:500]}"
            )
        # Broadcast to WebSocket clients
        asyncio.create_task(broadcast_notification(f"New Tender: {t.title} [{t.category}]"))
    db.close()