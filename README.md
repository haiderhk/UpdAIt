# UpdAIt: Stay Updated with the Latest in AI

UpdAIt is an iOS application that keeps users up-to-date with the latest developments in artificial intelligence. By leveraging RAG (Retrieval-Augmented Generation) technology, it is designed to enhance how users interact with and learn from the latest articles in AI.  
All articles featured in UpdAIt are extracted from [DeepLearning.AI's The Batch](https://www.deeplearning.ai/the-batch/). We are grateful for their incredible work in curating and publishing cutting-edge content in the field of artificial intelligence.

## 🌟 Features

- 📚 **Scrape and Analyze Articles**: Articles from [DeepLearning.AI's The Batch](https://www.deeplearning.ai/the-batch/) are scraped, chunked, and stored in a vector database for enhanced information retrieval.
- 🤖 **Ask AI**: Ask questions about any article and receive AI-powered responses based on relevant content and references.
- ❓ **Generate Questions**: Generate practice questions from specific articles to test your understanding
- 🌐 **Vector Search**: Utilizes **ChromaDB** for efficient similarity search and retrieval
- 📱 **Modern UI/UX**: Built with **SwiftUI** for iOS frontend and **FastAPI** for backend services

## 🛠️ Technical Stack

### Frontend (SwiftUI)

- **Modern and Minimal Design**: An interactive UI featuring gradients, animations, and user-focused design principles.
- **Architecture**: MVVM architecture pattern
- **Networking**: Native IOS networking layer for communication with REST API.

### Backend (Python)

- **FastAPI**: Used for RESTful API development
- **Pydantic**: Pydantic classes for data validation, structured output from LLM, and settings management.
- **LangChain**: Used for intelligent Text Splitting and Chunking, LLM Chain Management, Vector Store operations, and Prompt Management
- **ChromaDB**: A persistent vector database for efficient storage and retrieval of article chunks
- **Beautiful Soup**: Used for web scraping.

## 🚀 Deployment

UpdAIt implements a sophisticated deployment strategy utilizing Docker containerization and automated CI/CD pipelines through GitHub Actions. The application is deployed on **AWS** infrastructure, ensuring scalability and reliability.

### CI/CD Pipeline Overview

The project maintains two parallel CI/CD pipelines, each serving a specific purpose:

#### AWS Production Deployment (ECR + ECS)

1.  Checks out the latest code from the repository
2.  Configures AWS credentials securly using repository secrets
3.  Logs in to Amazon Elastic Container Registry (ECS)
4.  Builds and tags a Docker image with the latest changes
5.  Pushes the image to an Amazon ECR repository
6.  Triggers a deployment on Amazon ECS cluster

#### Docker Hub

Maintains a parallel image repository for version tracking.

1. Authenticates with DockerHub using secure credentials
2. Builds the Docker image with necessary build arguments
3. Pushes the tagged image to DockerHub
4. Includes secure handling of sensitive information like API keys

## 👨🏻‍💻 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/haiderhk/UpdAIt.git
```

### 2. Backend Setup

#### Run Locally

Navigate to the backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
python -m backend.app.main
```

Access the API documentation:
http://127.0.0.1:8000/docs

#### Run Using Docker

_Before proceeding, please ensure Docker is installed on your system_.

Build the docker image:

```bash
docker build -t image-name .
```

Run the docker container with your OpenAI API key:

```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your_openai_api_key image-name
```

Access the API documentation:
http://127.0.0.1:8000/docs

### 3. Frontend Setup

#### Requirements

macOS with Xcode installed.

#### Steps

1. Open the frontend folder in Xcode.
2. Build and run the project on a simulator or a connected iOS device.

## 📱App Showcase

### ✨ Demo Video

Watch UpdAIt in action: [View Full Demo](https://www.youtube.com/watch?v=IGxbcbiQzRY)

### Key Features

#### Home Screen: View the Latest Articles in AI

<table> <tr> <td width="50%"> <img src="assets/HomeScreen.PNG" alt="Home Screen" width="100%"> <p align="center">Static View</p> </td> <td width="50%"> <img src="assets/homescreen.gif" alt="Home Screen Animation" width="100%"> <p align="center">Article Swipe Animation</p> </td> </tr> </table>
