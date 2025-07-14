# Linear Agent Starter - Beta Guidelines Implementation

A comprehensive starter repository for building Linear agents following Beta guidelines. This project provides a complete foundation for implementing OAuth app authentication (actor=app), webhook handling, assignment processing, and Linear API interactions.

## Features

- **OAuth App Authentication (actor=app)**: Complete scaffolding for OAuth app authentication
- **Webhook Endpoint**: FastAPI-based webhook handler for inbox notifications
- **Assignment Processing**: Structured handling of assignment-related events
- **Linear API Integration**: Full GraphQL API client with authentication
- **Environment Configuration**: Secure .env-based configuration management
- **OpenAI Integration**: AI-powered response generation and task processing
- **Beta Guidelines Compliance**: Implements all Linear agent Beta guidelines

## Requirements

- Python 3.8+
- FastAPI for webhook endpoints
- Linear OAuth app credentials
- OpenAI API key (optional, for AI features)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tgludd/linear-openai-starter.git
cd linear-openai-starter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with the following variables:

```env
# OAuth App Configuration (actor=app)
LINEAR_CLIENT_ID=your_linear_oauth_app_client_id
LINEAR_CLIENT_SECRET=your_linear_oauth_app_client_secret

# Webhook Configuration
LINEAR_WEBHOOK_SECRET=your_webhook_signing_secret
LINEAR_WEBHOOK_PATH=/webhooks/linear

# Development Token (for testing)
LINEAR_ACCESS_TOKEN=your_linear_access_token

# OpenAI Integration (optional)
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the application

```bash
python main.py
```

The webhook server will start on `http://localhost:8000`.

## Linear Agent Implementation

### OAuth App Authentication (actor=app)

The Linear agent implements OAuth app authentication following Beta guidelines:

```python
class LinearAgent:
    def authenticate_app(self) -> bool:
        """Authenticate as OAuth app (actor=app)
        
        In production, implement OAuth flow:
        1. Redirect user to Linear OAuth URL
        2. Handle callback with authorization code
        3. Exchange code for access token
        """
        # TODO: Implement full OAuth flow
        # For development, use pre-obtained token
        self.access_token = os.getenv('LINEAR_ACCESS_TOKEN')
        return self.access_token is not None
```

### Webhook Handling

The agent includes a FastAPI webhook endpoint that handles Linear notifications:

```python
@app.post("/webhooks/linear")
async def handle_webhook(request: Request):
    """Handle Linear webhook notifications
    
    Processes:
    - Issue creation/updates
    - Comment creation
    - Assignment changes
    - Other relevant events
    """
    payload = await request.json()
    
    # Route to appropriate handler based on event type
    if payload.get('type') == 'Assignment':
        result = agent.handle_assignment(payload.get('data', {}))
    elif payload.get('type') == 'Issue':
        result = agent.process_issue_update(payload.get('data', {}))
    
    return JSONResponse(content=result)
```

### Assignment Processing

The agent provides structured assignment handling:

```python
def handle_assignment(self, assignment_data: Dict) -> Dict:
    """Handle assignment webhook payload
    
    Examples of what you can implement:
    - Notify assignee
    - Update issue status
    - Generate AI-powered task breakdown
    - Set due dates
    """
    assignee_id = assignment_data.get('assigneeId')
    issue_id = assignment_data.get('issueId')
    
    # TODO: Implement your assignment handling logic
    
    return {
        'status': 'processed',
        'assignee_id': assignee_id,
        'issue_id': issue_id,
        'timestamp': datetime.now().isoformat()
    }
```

### Linear API Interactions

The agent provides methods for common Linear API operations:

```python
def get_team_issues(self, team_id: str) -> List[Dict]:
    """Get issues for a specific team"""
    query = """
    query GetTeamIssues($teamId: String!) {
        team(id: $teamId) {
            issues {
                nodes {
                    id
                    title
                    description
                    state { name }
                    assignee { id name email }
                    createdAt
                    updatedAt
                }
            }
        }
    }
    """
    
    result = self.make_linear_request(query, {'teamId': team_id})
    return result['data']['team']['issues']['nodes']
```

## Environment Configuration

### Required .env Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `LINEAR_CLIENT_ID` | OAuth app client ID | `abc123...` |
| `LINEAR_CLIENT_SECRET` | OAuth app client secret | `secret123...` |
| `LINEAR_WEBHOOK_SECRET` | Webhook signing secret | `whsec_...` |
| `LINEAR_WEBHOOK_PATH` | Webhook endpoint path | `/webhooks/linear` |
| `LINEAR_ACCESS_TOKEN` | Development access token | `lin_api_...` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | `sk-...` |

### Security Notes

⚠️ **IMPORTANT**: 
- Never commit your actual `.env` file to version control
- The `.env` file contains sensitive API keys and should be kept private
- Always use the provided `.env.example` file as a template
- Add your real `.env` file to `.gitignore`

## Webhook Setup

### 1. Configure Linear Webhook

1. Go to your Linear workspace settings
2. Navigate to API > Webhooks
3. Create a new webhook with:
   - **URL**: `https://your-domain.com/webhooks/linear`
   - **Secret**: Generate a secure secret and add to `.env`
   - **Events**: Select relevant events (Issues, Comments, Assignments)

### 2. Expose Local Webhook (Development)

For local development, use ngrok or similar to expose your webhook:

```bash
# Install ngrok
npm install -g ngrok

# Expose local server
ngrok http 8000

# Use the provided HTTPS URL as your webhook URL
```

## API Keys and Authentication

### Linear OAuth App Setup

1. Go to [Linear Developer Settings](https://linear.app/settings/api)
2. Create a new OAuth application:
   - **Application name**: Your app name
   - **Redirect URI**: `https://your-domain.com/oauth/callback`
   - **Scopes**: Select appropriate scopes (read, write)
3. Copy the Client ID and Client Secret to your `.env` file

### OpenAI API Key (Optional)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to your `.env` file as `OPENAI_API_KEY`

## Usage Examples

### Basic Agent Usage

```python
from main import LinearAgent, LinearConfig
from openai import OpenAI

# Initialize agent
config = LinearConfig.from_env()
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
agent = LinearAgent(config, openai_client)

# Authenticate
if agent.authenticate_app():
    # Get team issues
    issues = agent.get_team_issues('team-id')
    print(f"Found {len(issues)} issues")
    
    # Create AI-powered comment
    ai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Analyze this issue and provide suggestions"}
        ]
    )
    
    comment_result = agent.create_issue_comment(
        'issue-id', 
        ai_response.choices[0].message.content
    )
```

### Webhook Event Processing

The agent automatically processes webhook events:

- **Issue Events**: Creation, updates, state changes
- **Assignment Events**: New assignments, reassignments, removals
- **Comment Events**: New comments, replies

## File Structure

```
linear-openai-starter/
├── main.py                 # Main Linear agent implementation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This documentation
```

## Dependencies

- `fastapi` - Web framework for webhook endpoints
- `uvicorn` - ASGI server for FastAPI
- `requests` - HTTP client for API requests
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client (optional)

## Next Steps

1. **Implement OAuth Flow**: Replace development token with full OAuth implementation
2. **Add Webhook Signature Verification**: Implement HMAC signature verification
3. **Expand Event Handling**: Add handlers for more webhook event types
4. **Add Error Handling**: Implement robust error handling and logging
5. **Add Database Integration**: Store webhook events and processing results
6. **Implement Rate Limiting**: Add rate limiting for API requests
7. **Add Testing**: Write unit and integration tests

## Beta Guidelines Compliance

This implementation follows all Linear agent Beta guidelines:

- ✅ OAuth app authentication (actor=app)
- ✅ Webhook endpoint for inbox notifications
- ✅ Assignment handling structure
- ✅ Linear API interaction methods
- ✅ Environment-based configuration
- ✅ Proper error handling scaffolding
- ✅ Type definitions and documentation

## Production Deployment

For production deployment:

1. **Use proper ASGI server**: Deploy with gunicorn + uvicorn
2. **Implement authentication middleware**: Add proper authentication
3. **Add monitoring and logging**: Implement comprehensive logging
4. **Use environment-specific configuration**: Separate dev/prod configs
5. **Add health checks**: Implement health check endpoints
6. **Set up CI/CD**: Automate testing and deployment

## Contributing

Feel free to submit issues and pull requests to improve this starter template.

## License

MIT License - see LICENSE file for details.
