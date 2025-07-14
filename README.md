# Linear OpenAI Starter

A starter repository for integrating Linear project management with OpenAI API. This project provides a foundation for building applications that combine Linear's issue tracking capabilities with OpenAI's AI-powered features.

## Features

- **Linear API Integration**: Connect to Linear's GraphQL API to manage issues, teams, and projects
- **OpenAI API Integration**: Leverage OpenAI's AI capabilities for intelligent task processing
- **Environment-based Configuration**: Secure API key management using environment variables
- **Example Functions**: Ready-to-use functions for common Linear and OpenAI operations

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tgludd/linear-openai-starter.git
   cd linear-openai-starter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file or set the following environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   LINEAR_API_KEY=your_linear_api_key_here
   ```

4. **Run the example**:
   ```bash
   python main.py
   ```

## Usage

### Installation and Setup

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   LINEAR_API_KEY=your_linear_api_key_here
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Security Note

**⚠️ IMPORTANT**: Never commit your actual `.env` file to version control. The `.env` file contains sensitive API keys and should be kept private. Always use the provided `.env.example` file as a template and add your real `.env` file to `.gitignore`.

## API Keys

- **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Linear API Key**: Generate a personal API key from [Linear Settings](https://linear.app/settings/api)

## Usage Examples

### Linear API
- Get team information
- Create and manage issues
- Query project data

### OpenAI API
- Generate intelligent responses
- Process and analyze text
- Automate task descriptions

## Files

- `main.py`: Main application with API client initialization and example functions
- `requirements.txt`: Python dependencies (openai, requests)
- `.gitignore`: Python-specific gitignore rules
- `README.md`: This documentation

## Next Steps

1. Explore the Linear GraphQL API documentation
2. Experiment with OpenAI's various models and capabilities
3. Build custom integrations combining both APIs
4. Add error handling and logging for production use

## Contributing

Feel free to submit issues and pull requests to improve this starter template.

## License

MIT License - see LICENSE file for details.
