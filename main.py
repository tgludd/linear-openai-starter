import os
import requests
from openai import OpenAI

# Initialize OpenAI client with environment variable
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

# Linear API configuration
LINEAR_API_URL = 'https://api.linear.app/graphql'
LINEAR_API_KEY = os.getenv('LINEAR_API_KEY')

# Initialize Linear client using requests
def linear_request(query, variables=None):
    """Make a GraphQL request to Linear API"""
    headers = {
        'Authorization': f'Bearer {LINEAR_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'query': query,
        'variables': variables or {}
    }
    
    response = requests.post(LINEAR_API_URL, json=payload, headers=headers)
    return response.json()

# Example usage functions
def get_linear_teams():
    """Get teams from Linear"""
    query = '''
    query {
        teams {
            nodes {
                id
                name
                description
            }
        }
    }
    '''
    return linear_request(query)

def chat_with_openai(message):
    """Chat with OpenAI"""
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    # Example usage
    print("Linear and OpenAI API Integration Starter")
    print("==========================================")
    
    # Check if API keys are set
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set")
    
    if not os.getenv('LINEAR_API_KEY'):
        print("Warning: LINEAR_API_KEY environment variable not set")
    
    # Example: Get Linear teams (if API key is set)
    if LINEAR_API_KEY:
        try:
            teams = get_linear_teams()
            print(f"\nLinear teams: {teams}")
        except Exception as e:
            print(f"Error fetching Linear teams: {e}")
    
    # Example: Chat with OpenAI (if API key is set)
    if os.getenv('OPENAI_API_KEY'):
        try:
            response = chat_with_openai("Hello, how can I integrate Linear with OpenAI?")
            print(f"\nOpenAI response: {response}")
        except Exception as e:
            print(f"Error with OpenAI: {e}")
