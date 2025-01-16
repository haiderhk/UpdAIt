<h1 align="center">
UpdAIt: Stay Updated with the Latest in AI
</h1>

UpdAIt is an iOS application that keeps users up-to-date with the latest developments in artificial intelligence. By leveraging RAG (Retrieval-Augmented Generation) technology, it is designed to enhance how users interact with and learn from the latest articles in AI.

All articles featured in UpdAIt are extracted from [DeepLearning.AI's The Batch](https://www.deeplearning.ai/the-batch/). We are grateful for their incredible work in curating and publishing cutting-edge content in the field of artificial intelligence.

![Questions Screen-4](https://github.com/user-attachments/assets/37bd4620-d691-4abb-98fd-b40fcf89ef68)

## Table of Contents

- [🌟 Features](#-features)
- [🛠️ Technical Stack](#️-technical-stack)
  - [Frontend (SwiftUI)](#frontend-swiftui)
  - [Backend (Python)](#backend-python)
- [🚀 Deployment](#-deployment)
  - [CI/CD Pipeline Overview](#cicd-pipeline-overview)
  - [AWS Production Deployment (ECR + ECS)](#aws-production-deployment-ecr--ecs)
  - [Docker Hub](#docker-hub)
- [👨🏻‍💻 Getting Started](#-getting-started)
  1. [Clone the Repository](#1-clone-the-repository)
  2. [Backend Setup](#2-backend-setup)
     - [Run Locally](#run-locally)
     - [Run Using Docker](#run-using-docker)
  3. [Frontend Setup](#3-frontend-setup)
     - [Requirements](#requirements)
     - [Steps](#steps)
- [📱App Showcase](#app-showcase)
  - [✨ Demo Video](#-demo-video)
  - [Key Features and Interfaces](#key-features-and-interfaces)
- [🔮 Future Improvements](#-future-improvements)
- [🙏 Acknowledgements](#-acknowledgements)

## 🌟 Features

- 📚 **Scrape and Analyze Articles**: Articles from [DeepLearning.AI's The Batch](https://www.deeplearning.ai/the-batch/) are scraped, chunked, and stored in a vector database for enhanced information retrieval

- 🤖 **Ask AI**: Ask questions about any article and receive AI-powered responses based on relevant content and references

- ❓ **Generate Questions**: Generate practice questions from specific articles to test your understanding

- 🌐 **Vector Search**: Utilizes **ChromaDB** for efficient similarity search and retrieval

- 📱 **Modern UI/UX**: Built with **SwiftUI** for iOS frontend and **FastAPI** for backend services

---

## 🛠️ Technical Stack

### Frontend (SwiftUI)

- **Modern and Minimal Design**: An interactive UI featuring gradients, animations, and user-focused design principles

- **Architecture**: MVVM architecture pattern

- **Networking**: Native iOS networking layer for communication with REST API

### Backend (Python)

- **FastAPI**: Used for RESTful API development

- **Pydantic**: Pydantic classes for data validation, structured output from LLM, and settings management

- **LangChain**: Used for intelligent Text Splitting and Chunking, LLM Chain Management for retrieval augmented generation, Vector Store operations, and Prompt Management

- **ChromaDB**: A persistent vector database for efficient storage and retrieval of article chunks

- **Beautiful Soup**: Used for web scraping

---

## 🚀 Deployment

UpdAIt implements a sophisticated deployment strategy utilizing Docker containerization and automated CI/CD pipelines through GitHub Actions. The application is deployed on **AWS** infrastructure, ensuring scalability and reliability.

### CI/CD Pipeline Overview

The project maintains two parallel CI/CD pipelines, each serving a specific purpose:

#### AWS Production Deployment (ECR + ECS)

1. Checks out the latest code from the repository

2. Configures AWS credentials securely using repository secrets

3. Logs in to Amazon Elastic Container Registry (ECR)

4. Builds and tags a Docker image with the latest changes

5. Pushes the image to an Amazon ECR repository

6. Triggers a deployment on Amazon ECS cluster

#### Docker Hub

Maintains a parallel image repository for version tracking.

1. Authenticates with DockerHub using secure credentials

2. Builds the Docker image with necessary build arguments

3. Pushes the tagged image to DockerHub

4. Includes secure handling of sensitive information like API keys

---

## 👨🏻‍💻 Getting Started

### 1. Clone the Repository

```bash

git  clone  https://github.com/haiderhk/UpdAIt.git

```

### 2. Backend Setup

#### Run Locally

Create Python Virtual Environment and Install dependencies:

```bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Navigate to the backend folder:

```bash

cd  backend

```

Start the backend server:

```bash

python  -m  backend.app.main

```

Access the API documentation:

http://127.0.0.1:8000/docs

#### Run Using Docker

_Before proceeding, please ensure Docker is installed on your system_.

Build the Docker image:

```bash

docker  build  -t  image-name  .

```

Run the docker container with your OpenAI API key:

```bash

docker  run  -p  8000:8000  -e  OPENAI_API_KEY=your_openai_api_key  image-name

```

_For production deployments, avoid hardcoding API keys in commands. Use environment variables managed by your CI/CD pipeline or container orchestration platform (e.g., ECS)._

Access the API documentation:

http://127.0.0.1:8000/docs

### 3. Frontend Setup

#### Requirements

macOS with Xcode installed.

#### Steps

1. Open the frontend folder in Xcode.

2. Build and run the project on a simulator or a connected iOS device.

---

## 📱App Showcase

### ✨ Demo Video

Watch UpdAIt in action: [View Full Demo](https://youtu.be/nwUFBrAui4Q)

### Key Features and Interfaces

#### Home Screen

![UpdAIt-GitHub-Screenshots-Videos](https://github.com/user-attachments/assets/a64dd971-2399-4e83-8bba-863cc20e025f)

The home screen offers a sleek, card-based interface for browsing the latest articles in AI.  
All articles are sourced from [DeepLearning.AI's The Batch](https://www.deeplearning.ai/the-batch/).

#### Retrieval and Questions Screen

![UpdAIt-GitHub-Screenshots-Videos-2-2](https://github.com/user-attachments/assets/6138a584-b994-42bd-a18e-fa930e4ad145)

- The **retrieval** interface showcases the power of RAG technology, presenting AI-generated answers alongside source references. The user can access the original articles that contributed to the response.
- The **questions** screen showcases the AI's ability to generate practice questions from an article to enhance learning. The user can enter their answer or reveal the AI's answer from the article.

---

## 🔮 Future Improvements

- Support for additional AI content sources
- Push notifications for new articles
- User preferences and personalization

---

## 🙏 Acknowledgements

- [DeepLearning.AI](https://www.deeplearning.ai) for their incredible work on _The Batch_, which serves as the core content source for this application.
- The open-source community behind the amazing tools and frameworks that powered this app:
  - [FastAPI](https://fastapi.tiangolo.com) for building a high-performance backend API.
  - [LangChain](https://www.langchain.com) for enabling seamless retrieval-augmented generation (RAG) capabilities.
  - [ChromaDB](https://www.trychroma.com) for providing a robust vector database for AI-powered search and retrieval.
