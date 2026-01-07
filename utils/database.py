"""
Database management for video production system.

Uses SQLite to store projects, videos, agent logs, and YouTube channel data.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from config.settings import DATABASE_PATH


class Database:
    """SQLite database manager for video production system."""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialize database connection and create tables."""
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                user_idea TEXT NOT NULL,
                style TEXT,
                duration INTEGER,
                format TEXT,
                production_plan TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                video_path TEXT,
                thumbnail_path TEXT,
                title TEXT,
                description TEXT,
                hashtags TEXT,
                duration REAL,
                format TEXT,
                status TEXT DEFAULT 'processing',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        
        # Agents log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                agent_name TEXT NOT NULL,
                status TEXT DEFAULT 'running',
                input_data TEXT,
                output_data TEXT,
                error_message TEXT,
                execution_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        
        # YouTube channels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS youtube_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_url TEXT UNIQUE NOT NULL,
                channel_name TEXT,
                analysis_data TEXT,
                videos_data TEXT,
                insights TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    # Project methods
    def create_project(
        self,
        project_name: str,
        user_idea: str,
        style: str,
        duration: int,
        format: str,
        production_plan: Optional[Dict[str, Any]] = None
    ) -> int:
        """Create a new project and return its ID."""
        cursor = self.conn.cursor()
        production_plan_json = json.dumps(production_plan) if production_plan else None
        
        cursor.execute("""
            INSERT INTO projects (project_name, user_idea, style, duration, format, production_plan)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (project_name, user_idea, style, duration, format, production_plan_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        
        if row:
            project = dict(row)
            if project.get("production_plan"):
                project["production_plan"] = json.loads(project["production_plan"])
            return project
        return None
    
    def update_project_status(self, project_id: int, status: str):
        """Update project status."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE projects 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (status, project_id))
        self.conn.commit()
    
    def update_project_plan(self, project_id: int, production_plan: Dict[str, Any]):
        """Update project production plan."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE projects 
            SET production_plan = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (json.dumps(production_plan), project_id))
        self.conn.commit()
    
    def list_projects(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all projects, optionally filtered by status."""
        cursor = self.conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM projects WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        
        rows = cursor.fetchall()
        projects = [dict(row) for row in rows]
        
        for project in projects:
            if project.get("production_plan"):
                try:
                    project["production_plan"] = json.loads(project["production_plan"])
                except:
                    project["production_plan"] = None
        
        return projects
    
    # Video methods
    def create_video(
        self,
        project_id: int,
        video_path: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        hashtags: Optional[List[str]] = None,
        duration: Optional[float] = None,
        format: Optional[str] = None,
        thumbnail_path: Optional[str] = None
    ) -> int:
        """Create a new video record."""
        cursor = self.conn.cursor()
        hashtags_json = json.dumps(hashtags) if hashtags else None
        
        cursor.execute("""
            INSERT INTO videos (project_id, video_path, thumbnail_path, title, description, 
                              hashtags, duration, format, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'completed')
        """, (project_id, video_path, thumbnail_path, title, description, 
              hashtags_json, duration, format))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_video(self, video_id: int) -> Optional[Dict[str, Any]]:
        """Get video by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        
        if row:
            video = dict(row)
            if video.get("hashtags"):
                try:
                    video["hashtags"] = json.loads(video["hashtags"])
                except:
                    video["hashtags"] = []
            return video
        return None
    
    def list_videos(self, project_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List videos, optionally filtered by project_id or status."""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM videos WHERE 1=1"
        params = []
        
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        videos = [dict(row) for row in rows]
        
        for video in videos:
            if video.get("hashtags"):
                try:
                    video["hashtags"] = json.loads(video["hashtags"])
                except:
                    video["hashtags"] = []
        
        return videos
    
    def update_video_status(self, video_id: int, status: str):
        """Update video status."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE videos 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (status, video_id))
        self.conn.commit()
    
    # Agent log methods
    def log_agent_start(self, project_id: int, agent_name: str, input_data: Optional[Dict[str, Any]] = None) -> int:
        """Log agent start and return log ID."""
        cursor = self.conn.cursor()
        input_json = json.dumps(input_data) if input_data else None
        
        cursor.execute("""
            INSERT INTO agents_log (project_id, agent_name, status, input_data)
            VALUES (?, ?, 'running', ?)
        """, (project_id, agent_name, input_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def log_agent_complete(
        self,
        log_id: int,
        output_data: Optional[Dict[str, Any]] = None,
        execution_time: Optional[float] = None
    ):
        """Log agent completion."""
        cursor = self.conn.cursor()
        output_json = json.dumps(output_data) if output_data else None
        
        cursor.execute("""
            UPDATE agents_log 
            SET status = 'completed', output_data = ?, execution_time = ?
            WHERE id = ?
        """, (output_json, execution_time, log_id))
        
        self.conn.commit()
    
    def log_agent_error(self, log_id: int, error_message: str):
        """Log agent error."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE agents_log 
            SET status = 'error', error_message = ?
            WHERE id = ?
        """, (error_message, log_id))
        
        self.conn.commit()
    
    def get_agent_logs(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all agent logs for a project."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM agents_log 
            WHERE project_id = ? 
            ORDER BY created_at ASC
        """, (project_id,))
        
        rows = cursor.fetchall()
        logs = []
        
        for row in rows:
            log = dict(row)
            if log.get("input_data"):
                try:
                    log["input_data"] = json.loads(log["input_data"])
                except:
                    pass
            if log.get("output_data"):
                try:
                    log["output_data"] = json.loads(log["output_data"])
                except:
                    pass
            logs.append(log)
        
        return logs
    
    # YouTube channel methods
    def save_youtube_channel(
        self,
        channel_url: str,
        channel_name: Optional[str] = None,
        analysis_data: Optional[Dict[str, Any]] = None,
        videos_data: Optional[List[Dict[str, Any]]] = None,
        insights: Optional[str] = None
    ):
        """Save or update YouTube channel data."""
        cursor = self.conn.cursor()
        analysis_json = json.dumps(analysis_data) if analysis_data else None
        videos_json = json.dumps(videos_data) if videos_data else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO youtube_channels 
            (channel_url, channel_name, analysis_data, videos_data, insights, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (channel_url, channel_name, analysis_json, videos_json, insights))
        
        self.conn.commit()
    
    def get_youtube_channel(self, channel_url: str) -> Optional[Dict[str, Any]]:
        """Get YouTube channel data by URL."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM youtube_channels WHERE channel_url = ?", (channel_url,))
        row = cursor.fetchone()
        
        if row:
            channel = dict(row)
            if channel.get("analysis_data"):
                try:
                    channel["analysis_data"] = json.loads(channel["analysis_data"])
                except:
                    pass
            if channel.get("videos_data"):
                try:
                    channel["videos_data"] = json.loads(channel["videos_data"])
                except:
                    pass
            return channel
        return None
    
    def list_youtube_channels(self) -> List[Dict[str, Any]]:
        """List all YouTube channels."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM youtube_channels ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        
        channels = []
        for row in rows:
            channel = dict(row)
            if channel.get("analysis_data"):
                try:
                    channel["analysis_data"] = json.loads(channel["analysis_data"])
                except:
                    pass
            if channel.get("videos_data"):
                try:
                    channel["videos_data"] = json.loads(channel["videos_data"])
                except:
                    pass
            channels.append(channel)
        
        return channels
    
    def close(self):
        """Close database connection."""
        self.conn.close()


# Global database instance
_db_instance: Optional[Database] = None

def get_db() -> Database:
    """Get or create global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance


# Simplified helper functions for MVP
def log_agent_action(project_id: int, agent_name: str, message: str):
    """Simplified logging function for agent actions."""
    db = get_db()
    log_id = db.log_agent_start(project_id, agent_name, {"message": message})
    db.log_agent_complete(log_id, {"message": message})


def create_project(topic: str, style: str = "Industrial") -> int:
    """Simplified project creation function."""
    db = get_db()
    project_name = f"Video_{topic[:30]}"
    return db.create_project(
        project_name=project_name,
        user_idea=topic,
        style=style,
        duration=60,
        format="Vertical 9:16"
    )


def update_project_script(project_id: int, script_content):
    """Guarda el guion generado en la base de datos."""
    import sqlite3
    from config.settings import DATABASE_PATH
    
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    # Guardamos el script como texto (JSON string)
    c.execute(
        "UPDATE projects SET production_plan = ?, status = 'scripted' WHERE id = ?", 
        (json.dumps(script_content), project_id)
    )
    conn.commit()
    conn.close()


def update_scene_image(project_id: int, scene_number: int, image_path: str):
    """Guarda la ruta de la imagen generada para una escena específica."""
    import sqlite3
    from config.settings import DATABASE_PATH
    
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    
    # Recuperar el script actual
    c.execute("SELECT production_plan FROM projects WHERE id = ?", (project_id,))
    row = c.fetchone()
    
    if row and row[0]:
        script = json.loads(row[0])
        
        # Buscar la escena y añadir el campo 'image_path'
        for scene in script:
            if scene.get('scene_number') == scene_number:
                scene['image_path'] = str(image_path)
                break
        
        # Guardar el script actualizado
        c.execute(
            "UPDATE projects SET production_plan = ? WHERE id = ?", 
            (json.dumps(script), project_id)
        )
        conn.commit()
    
    conn.close()


def update_scene_audio(project_id: int, scene_number: int, audio_path: str):
    """Guarda la ruta del audio generado para una escena específica."""
    import sqlite3
    from config.settings import DATABASE_PATH
    
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    
    # Recuperar el script actual
    c.execute("SELECT production_plan FROM projects WHERE id = ?", (project_id,))
    row = c.fetchone()
    
    if row and row[0]:
        script = json.loads(row[0])
        
        # Buscar la escena y añadir el campo 'audio_path'
        for scene in script:
            if scene.get('scene_number') == scene_number:
                scene['audio_path'] = str(audio_path)
                break
        
        # Guardar el script actualizado
        c.execute(
            "UPDATE projects SET production_plan = ? WHERE id = ?", 
            (json.dumps(script), project_id)
        )
        conn.commit()
    
    conn.close()
