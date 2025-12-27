"""
Integration with Tree of Life System (Node.js)

This module provides integration capabilities with the Tree of Life System
running as a separate Node.js service (github.com/Garrettc123/tree-of-life-system)
"""

import os
import logging
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class TreeOfLifeIntegration:
    """Integration client for Tree of Life System"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Tree of Life System integration
        
        Args:
            base_url: Base URL of the Tree of Life System API
                     Defaults to TREE_OF_LIFE_URL env variable or localhost
        """
        self.base_url = base_url or os.getenv(
            "TREE_OF_LIFE_URL", 
            "http://localhost:3000"
        )
        self.client = httpx.AsyncClient(base_url=self.base_url)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get Tree of Life System status"""
        try:
            response = await self.client.get("/api/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"error": str(e), "status": "unavailable"}
    
    async def sync_github_data(self, repo: str) -> Dict[str, Any]:
        """
        Sync data with GitHub through Tree of Life System
        
        Args:
            repo: Repository identifier (e.g., "owner/repo")
        """
        try:
            response = await self.client.post(
                "/api/github/sync",
                json={"repository": repo}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to sync GitHub data: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def sync_linear_data(self, project_id: str) -> Dict[str, Any]:
        """
        Sync data with Linear through Tree of Life System
        
        Args:
            project_id: Linear project identifier
        """
        try:
            response = await self.client.post(
                "/api/linear/sync",
                json={"project_id": project_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to sync Linear data: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def sync_notion_data(self, database_id: str) -> Dict[str, Any]:
        """
        Sync data with Notion through Tree of Life System
        
        Args:
            database_id: Notion database identifier
        """
        try:
            response = await self.client.post(
                "/api/notion/sync",
                json={"database_id": database_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to sync Notion data: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global integration instance
_integration: Optional[TreeOfLifeIntegration] = None


def get_integration() -> TreeOfLifeIntegration:
    """Get or create global Tree of Life integration instance"""
    global _integration
    if _integration is None:
        _integration = TreeOfLifeIntegration()
    return _integration


async def close_integration():
    """Close global Tree of Life integration"""
    global _integration
    if _integration is not None:
        await _integration.close()
        _integration = None
