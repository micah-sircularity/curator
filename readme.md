# CuratorAI

An intelligent experience curation system built with FastAPI and modern AI technologies. This service helps create personalized activity and experience recommendations based on user preferences and location.

## Features

- 🎯 Personalized experience generation
- 📍 Location-based activity recommendations
- 🖼️ AI-powered image generation for experiences
- 🔍 Smart search and matching algorithms
- 🚀 Fast and scalable API design

## Tech Stack

- Python 3.x
- FastAPI
- Pydantic for data validation
- AI/ML integrations
- Poetry for dependency management

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/curatorai.git
cd curatorai
```

2. Install dependencies:
```bash
# Using poetry (recommended)
poetry install

# Using pip
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the required API keys and configurations.

## Environment Variables

The following environment variables need to be set:

```bash
# API Keys
BRAVE_API_KEY=your_brave_api_key
EXA_API_KEY=your_exa_api_key
FIREWORKS_API_KEY=your_fireworks_api_key
APIFY_API_KEY=your_apify_api_key
RAPIDAPI_KEY=your_rapidapi_key

# S3 Storage
S3_ACCESS_KEY=your_s3_access_key
S3_SECRET_KEY=your_s3_secret_key
```

Make sure to create a `.env` file in the root directory with these variables before running the application.

4. Run the application:
```bash
python main.py
```

## API Documentation

The API provides the following main endpoints:

- `POST /curator/experiences`: Generate personalized experiences
- Detailed API documentation is available at `/docs` when running the server

## Project Structure

```
curatorai/
├── src/
│   └── curatorai/
│       ├── core/           # Core business logic and models
│       │   ├── curator.py
│       │   ├── generate_images.py
│       │   └── query_generations.py
│       ├── utils/          # Utility functions and helpers
│       │   ├── detail_extraction.py
│       │   └── process_results.py
│       └── config/         # Configuration and settings
│           └── fireworks_config.py
├── tests/
│   └── unit/              # Unit tests
├── docs/                  # Documentation
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── pyproject.toml        # Project dependencies and metadata
└── requirements.txt      # Pin-pointed dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.