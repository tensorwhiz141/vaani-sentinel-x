"""
WebSocket handler for real-time agent processing
Provides real-time updates and streaming responses
"""

from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def send_to_user(self, message: str, user_id: str):
        """Send a message to a specific user."""
        if user_id in self.user_connections:
            await self.send_personal_message(message, self.user_connections[user_id])
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.active_connections.remove(connection)

# Global connection manager
manager = ConnectionManager()

async def handle_websocket_message(websocket: WebSocket, message: Dict[str, Any]):
    """Handle incoming WebSocket messages and route to appropriate agents."""
    
    try:
        message_type = message.get('type')
        data = message.get('data', {})
        request_id = message.get('request_id', 'unknown')
        
        # Send acknowledgment
        await websocket.send_text(json.dumps({
            'type': 'ack',
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'message': 'Request received and processing started'
        }))
        
        # Route to appropriate handler based on message type
        if message_type == 'translate':
            await handle_translation_stream(websocket, data, request_id)
        elif message_type == 'generate_content':
            await handle_content_generation_stream(websocket, data, request_id)
        elif message_type == 'analyze_sentiment':
            await handle_sentiment_stream(websocket, data, request_id)
        elif message_type == 'ping':
            await websocket.send_text(json.dumps({
                'type': 'pong',
                'timestamp': datetime.now().isoformat()
            }))
        else:
            await websocket.send_text(json.dumps({
                'type': 'error',
                'request_id': request_id,
                'message': f'Unknown message type: {message_type}'
            }))
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await websocket.send_text(json.dumps({
            'type': 'error',
            'message': f'Error processing request: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }))

async def handle_translation_stream(websocket: WebSocket, data: Dict[str, Any], request_id: str):
    """Handle streaming translation requests."""
    
    try:
        text = data.get('text', '')
        target_languages = data.get('target_languages', ['hi'])
        
        # Send progress updates
        total_languages = len(target_languages)
        
        for i, lang in enumerate(target_languages):
            # Simulate translation processing
            await asyncio.sleep(0.5)  # Simulate processing time
            
            # Send progress update
            progress = (i + 1) / total_languages * 100
            await websocket.send_text(json.dumps({
                'type': 'progress',
                'request_id': request_id,
                'progress': progress,
                'current_language': lang,
                'message': f'Translating to {lang}...'
            }))
            
            # Send partial result
            translated_text = f"[{lang.upper()}] {text}"  # Simplified translation
            await websocket.send_text(json.dumps({
                'type': 'partial_result',
                'request_id': request_id,
                'language': lang,
                'translated_text': translated_text,
                'confidence': 0.85
            }))
        
        # Send completion
        await websocket.send_text(json.dumps({
            'type': 'complete',
            'request_id': request_id,
            'message': 'Translation completed successfully',
            'total_translations': total_languages
        }))
        
    except Exception as e:
        await websocket.send_text(json.dumps({
            'type': 'error',
            'request_id': request_id,
            'message': f'Translation error: {str(e)}'
        }))

async def handle_content_generation_stream(websocket: WebSocket, data: Dict[str, Any], request_id: str):
    """Handle streaming content generation requests."""
    
    try:
        content = data.get('content', '')
        platforms = data.get('platforms', ['instagram'])
        
        total_platforms = len(platforms)
        
        for i, platform in enumerate(platforms):
            # Simulate content generation
            await asyncio.sleep(0.8)
            
            # Send progress
            progress = (i + 1) / total_platforms * 100
            await websocket.send_text(json.dumps({
                'type': 'progress',
                'request_id': request_id,
                'progress': progress,
                'current_platform': platform,
                'message': f'Generating content for {platform}...'
            }))
            
            # Send generated content
            generated_content = f"[{platform.upper()}] {content} #trending #viral"
            await websocket.send_text(json.dumps({
                'type': 'partial_result',
                'request_id': request_id,
                'platform': platform,
                'generated_content': generated_content,
                'quality_score': 0.92
            }))
        
        # Send completion
        await websocket.send_text(json.dumps({
            'type': 'complete',
            'request_id': request_id,
            'message': 'Content generation completed',
            'total_generated': total_platforms
        }))
        
    except Exception as e:
        await websocket.send_text(json.dumps({
            'type': 'error',
            'request_id': request_id,
            'message': f'Content generation error: {str(e)}'
        }))

async def handle_sentiment_stream(websocket: WebSocket, data: Dict[str, Any], request_id: str):
    """Handle streaming sentiment analysis requests."""
    
    try:
        text = data.get('text', '')
        
        # Simulate sentiment analysis steps
        steps = [
            {'step': 'tokenization', 'message': 'Tokenizing text...'},
            {'step': 'emotion_detection', 'message': 'Detecting emotions...'},
            {'step': 'sentiment_scoring', 'message': 'Calculating sentiment scores...'},
            {'step': 'tone_analysis', 'message': 'Analyzing tone...'}
        ]
        
        for i, step in enumerate(steps):
            await asyncio.sleep(0.3)
            
            progress = (i + 1) / len(steps) * 100
            await websocket.send_text(json.dumps({
                'type': 'progress',
                'request_id': request_id,
                'progress': progress,
                'current_step': step['step'],
                'message': step['message']
            }))
        
        # Send final result
        await websocket.send_text(json.dumps({
            'type': 'result',
            'request_id': request_id,
            'sentiment': 'positive',
            'sentiment_score': 0.75,
            'emotions': ['joy', 'confidence'],
            'confidence': 0.88
        }))
        
        await websocket.send_text(json.dumps({
            'type': 'complete',
            'request_id': request_id,
            'message': 'Sentiment analysis completed'
        }))
        
    except Exception as e:
        await websocket.send_text(json.dumps({
            'type': 'error',
            'request_id': request_id,
            'message': f'Sentiment analysis error: {str(e)}'
        }))

async def websocket_endpoint(websocket: WebSocket, user_id: str = None):
    """Main WebSocket endpoint handler."""
    
    await manager.connect(websocket, user_id)
    
    try:
        # Send welcome message
        await websocket.send_text(json.dumps({
            'type': 'welcome',
            'message': 'Connected to Vaani Sentinel-X Real-time Agent API',
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'available_types': ['translate', 'generate_content', 'analyze_sentiment', 'ping']
        }))
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                await handle_websocket_message(websocket, message)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON format'
                }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"WebSocket disconnected for user: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)
