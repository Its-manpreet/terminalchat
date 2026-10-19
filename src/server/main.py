# JUST MOCKUP

from datetime import datetime, timezone
from typing import Dict, List, Set

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI(title="Chat API")


class MessageCreate(BaseModel):
	user: str
	text: str


class Message(MessageCreate):
	id: int
	created_at: datetime


messages: Dict[str, List[Message]] = {}


class ConnectionManager:
	def __init__(self) -> None:
		self.connections: Dict[str, Set[WebSocket]] = {}

	async def connect(self, chat_id: str, websocket: WebSocket) -> None:
		await websocket.accept()
		self.connections.setdefault(chat_id, set()).add(websocket)

	def disconnect(self, chat_id: str, websocket: WebSocket) -> None:
		chat_connections = self.connections.get(chat_id)
		if chat_connections is None:
			return
		chat_connections.discard(websocket)
		if not chat_connections:
			self.connections.pop(chat_id, None)

	async def broadcast(self, chat_id: str, event: dict) -> None:
		for websocket in list(self.connections.get(chat_id, set())):
			try:
				await websocket.send_json(event)
			except Exception:
				self.disconnect(chat_id, websocket)


connection_manager = ConnectionManager()


@app.get("/health")
def health() -> dict:
	return {"status": "ok"}


@app.get("/chats/{chat_id}/messages", response_model=List[Message])
def list_messages(chat_id: str) -> List[Message]:
	return messages.get(chat_id, [])


@app.websocket("/ws/chats/{chat_id}")
async def chat_websocket(websocket: WebSocket, chat_id: str) -> None:
	await connection_manager.connect(chat_id, websocket)
	try:
		while True:
			await websocket.receive_text()
	except WebSocketDisconnect:
		connection_manager.disconnect(chat_id, websocket)


@app.post("/chats/{chat_id}/messages", response_model=Message, status_code=201)
async def send_message(chat_id: str, message: MessageCreate) -> Message:
	chat_messages = messages.setdefault(chat_id, [])
	new_message = Message(
		id=len(chat_messages) + 1,
		user=message.user,
		text=message.text,
		created_at=datetime.now(timezone.utc),
	)
	chat_messages.append(new_message)
	await connection_manager.broadcast(
		chat_id,
		{"type": "message.created", "message": jsonable_encoder(new_message)},
	)
	return new_message


@app.delete("/chats/{chat_id}/messages/{message_id}")
async def delete_message(chat_id: str, message_id: int) -> dict:
	chat_messages = messages.get(chat_id, [])
	for index, message in enumerate(chat_messages):
		if message.id == message_id:
			chat_messages.pop(index)
			await connection_manager.broadcast(
				chat_id,
				{"type": "message.deleted", "message_id": message_id},
			)
			return {"deleted": True}
	raise HTTPException(status_code=404, detail="Message not found")
