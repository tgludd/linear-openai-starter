"""Linear Agent Starter - Beta Guidelines Implementation

This starter code demonstrates how to build a Linear agent following Beta guidelines.
Implements OAuth (actor=app), webhook handling, assignment processing, and API interactions.

Key Components:
1. OAuth app authentication (actor=app)
2. Webhook endpoint for inbox notifications
3. Assignment handling
4. Linear API interactions
5. Environment-based configuration
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# FastAPI for webhook endpoint
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

# Environment configuration
from dotenv import load_dotenv

# HTTP client for API requests
import requests

# OpenAI integration
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


class WebhookEvent(Enum):
    """Webhook event types we handle"""
    ISSUE_CREATED = "Issue"
    ISSUE_UPDATED = "Issue"
    COMMENT_CREATED = "Comment"
    ASSIGNMENT_CREATED = "Assignment"
    ASSIGNMENT_UPDATED = "Assignment"
    ASSIGNMENT_DELETED = "Assignment"


@dataclass
class LinearConfig:
    """Configuration for Linear API and OAuth"""
    # OAuth configuration (actor=app)
    client_id: str
    client_secret: str
    
    # Webhook configuration
    webhook_secret: str
    webhook_path: str
    
    # API configuration
    api_url: str = "https://api.linear.app/graphql"
    
    @classmethod
    def from_env(cls) -> 'LinearConfig':
        """Load configuration from environment variables
        
        Required .env variables:
        - LINEAR_CLIENT_ID: OAuth app client ID
        - LINEAR_CLIENT_SECRET: OAuth app client secret
        - LINEAR_WEBHOOK_SECRET: Webhook signing secret
        - LINEAR_WEBHOOK_PATH: Webhook endpoint path (e.g., /webhooks/linear)
        """
        return cls(
            client_id=os.getenv('LINEAR_CLIENT_ID', ''),
            client_secret=os.getenv('LINEAR_CLIENT_SECRET', ''),
            webhook_secret=os.getenv('LINEAR_WEBHOOK_SECRET', ''),
            webhook_path=os.getenv('LINEAR_WEBHOOK_PATH', '/webhooks/linear')
        )


class LinearAgent:
    """Linear Agent implementing Beta guidelines
    
    This agent demonstrates:
    - OAuth app authentication (actor=app)
    - Webhook handling for inbox notifications
    - Assignment processing
    - API interactions
    """
    
    def __init__(self, config: LinearConfig, openai_client: OpenAI):
        self.config = config
        self.openai_client = openai_client
        self.access_token: Optional[str] = None
        
    def authenticate_app(self) -> bool:
        """Authenticate as OAuth app (actor=app)
        
        In production, implement OAuth flow:
        1. Redirect user to Linear OAuth URL
        2. Handle callback with authorization code
        3. Exchange code for access token
        
        For this starter, assuming you have a token from OAuth flow.
        """
        # TODO: Implement full OAuth flow
        # For now, use a pre-obtained token from environment
        self.access_token = os.getenv('LINEAR_ACCESS_TOKEN')
        return self.access_token is not None
    
    def make_linear_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Make authenticated GraphQL request to Linear API
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            GraphQL response data
        """
        if not self.access_token:
            raise Exception("Not authenticated. Call authenticate_app() first.")
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        response = requests.post(self.config.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def handle_assignment(self, assignment_data: Dict) -> Dict:
        """Handle assignment webhook payload
        
        Args:
            assignment_data: Assignment data from webhook
            
        Returns:
            Processing result
        """
        # Extract assignment details
        assignee_id = assignment_data.get('assigneeId')
        issue_id = assignment_data.get('issueId')
        
        # TODO: Implement assignment handling logic
        # Examples:
        # - Notify assignee
        # - Update issue status
        # - Generate AI-powered task breakdown
        # - Set due dates
        
        return {
            'status': 'processed',
            'assignee_id': assignee_id,
            'issue_id': issue_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_issue_update(self, issue_data: Dict) -> Dict:
        """Process issue update webhook
        
        Args:
            issue_data: Issue data from webhook
            
        Returns:
            Processing result
        """
        # TODO: Implement issue update processing
        # Examples:
        # - Generate AI responses to comments
        # - Auto-assign based on content
        # - Update labels/priorities
        # - Create sub-issues
        
        return {
            'status': 'processed',
            'issue_id': issue_data.get('id'),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_team_issues(self, team_id: str) -> List[Dict]:
        """Get issues for a specific team
        
        Args:
            team_id: Linear team ID
            
        Returns:
            List of issues
        """
        query = """
        query GetTeamIssues($teamId: String!) {
            team(id: $teamId) {
                issues {
                    nodes {
                        id
                        title
                        description
                        state {
                            name
                        }
                        assignee {
                            id
                            name
                            email
                        }
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """
        
        result = self.make_linear_request(query, {'teamId': team_id})
        return result['data']['team']['issues']['nodes']
    
    def create_issue_comment(self, issue_id: str, comment: str) -> Dict:
        """Create a comment on an issue
        
        Args:
            issue_id: Linear issue ID
            comment: Comment text
            
        Returns:
            Created comment data
        """
        mutation = """
        mutation CreateComment($issueId: String!, $body: String!) {
            commentCreate(input: {
                issueId: $issueId
                body: $body
            }) {
                success
                comment {
                    id
                    body
                    createdAt
                }
            }
        }
        """
        
        result = self.make_linear_request(mutation, {
            'issueId': issue_id,
            'body': comment
        })
        return result['data']['commentCreate']


# FastAPI app for webhook handling
app = FastAPI(title="Linear Agent Webhook Handler")

# Global agent instance
linear_config = LinearConfig.from_env()
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
agent = LinearAgent(linear_config, openai_client)


@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    if not agent.authenticate_app():
        raise Exception("Failed to authenticate Linear app")
    print("Linear Agent initialized successfully")


@app.post(linear_config.webhook_path)
async def handle_webhook(request: Request):
    """Handle Linear webhook notifications
    
    This endpoint receives webhook payloads from Linear for:
    - Issue creation/updates
    - Comment creation
    - Assignment changes
    - Other relevant events
    
    Webhook payload structure:
    {
        "action": "create" | "update" | "remove",
        "type": "Issue" | "Comment" | "Assignment",
        "data": { ... },
        "createdAt": "2023-...",
        "updatedAt": "2023-..."
    }
    """
    try:
        # Get webhook payload
        payload = await request.json()
        
        # TODO: Verify webhook signature using LINEAR_WEBHOOK_SECRET
        # signature = request.headers.get('Linear-Signature')
        # if not verify_signature(payload, signature, linear_config.webhook_secret):
        #     raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Extract event details
        event_type = payload.get('type')
        action = payload.get('action')
        data = payload.get('data', {})
        
        # Route to appropriate handler based on event type
        if event_type == 'Assignment':
            result = agent.handle_assignment(data)
        elif event_type == 'Issue':
            result = agent.process_issue_update(data)
        elif event_type == 'Comment':
            # TODO: Implement comment handling
            result = {'status': 'comment_processed'}
        else:
            result = {'status': 'unhandled', 'type': event_type}
        
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


def verify_signature(payload: Dict, signature: str, secret: str) -> bool:
    """Verify webhook signature
    
    Args:
        payload: Webhook payload
        signature: Signature from Linear-Signature header
        secret: Webhook secret from environment
        
    Returns:
        True if signature is valid
    """
    # TODO: Implement HMAC signature verification
    # import hmac
    # import hashlib
    # 
    # expected_signature = hmac.new(
    #     secret.encode(),
    #     json.dumps(payload).encode(),
    #     hashlib.sha256
    # ).hexdigest()
    # 
    # return hmac.compare_digest(signature, expected_signature)
    return True


if __name__ == '__main__':
    """
    Local development server
    
    To run locally:
    1. Create .env file with required variables
    2. Install dependencies: pip install -r requirements.txt
    3. Run: python main.py
    4. Use ngrok or similar to expose webhook endpoint
    
    For production deployment:
    - Use proper ASGI server (uvicorn, gunicorn)
    - Implement proper error handling and logging
    - Add authentication middleware
    - Use environment-specific configuration
    """
    import uvicorn
    
    print("Starting Linear Agent Webhook Server...")
    print(f"Webhook endpoint: {linear_config.webhook_path}")
    print("Environment variables required:")
    print("- LINEAR_CLIENT_ID")
    print("- LINEAR_CLIENT_SECRET")
    print("- LINEAR_WEBHOOK_SECRET")
    print("- LINEAR_WEBHOOK_PATH")
    print("- LINEAR_ACCESS_TOKEN (for development)")
    print("- OPENAI_API_KEY")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Example usage and testing functions
def example_usage():
    """Example usage of the Linear Agent"""
    
    # Initialize agent
    config = LinearConfig.from_env()
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    agent = LinearAgent(config, openai_client)
    
    # Authenticate
    if not agent.authenticate_app():
        print("Authentication failed")
        return
    
    # Example: Get team issues
    # team_id = "your-team-id"
    # issues = agent.get_team_issues(team_id)
    # print(f"Found {len(issues)} issues")
    
    # Example: Create comment with AI response
    # issue_id = "issue-id"
    # ai_response = openai_client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": "Generate a helpful comment for this issue"}
    #     ]
    # )
    # comment_result = agent.create_issue_comment(issue_id, ai_response.choices[0].message.content)
    # print(f"Comment created: {comment_result}")
    
    print("Example usage completed")


# Type definitions for better IDE support
WebhookPayload = Dict[str, Any]
IssueData = Dict[str, Any]
AssignmentData = Dict[str, Any]
CommentData = Dict[str, Any]
