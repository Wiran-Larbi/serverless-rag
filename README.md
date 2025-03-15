# Serverless RAG - AWS-Powered Document Intelligence

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/AWS-Powered-orange)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)

A scalable enterprise-grade document intelligence platform that combines the power of Large Language Models (LLMs) with AWS infrastructure to provide semantic search capabilities through Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **PDF-to-Knowledge Conversion Pipeline**: Transform documents into queryable knowledge
- **Context-Aware Q&A**: Get accurate answers with LLM synthesis
- **Zero-Downtime AWS Deployment**: Enterprise-grade reliability
- **Secure Access Control**: Role-based authentication
- **Vector-based Search**: High-performance semantic matching

## 🏗️ Architecture

The system operates in two main stages:

### Document Processing Pipeline

![RAG system architecture](/images/projects/project-serverlessrag/rag_architecture.png)

#### Stage 1: Ingestion & Preparation
1. **PDF Upload**: Users submit documents through admin interface
2. **Document Chunking**: Split PDFs into semantic text segments
3. **Vector Encoding**: Convert chunks to embeddings using Amazon Titan model
4. **Vector Storage**: Index embeddings in FAISS with metadata pointers

#### Stage 2: Question Answering
1. **Query Input**: Receive natural language question from user
2. **Query Encoding**: Convert question to vector using Tim model
3. **Context Retrieval**: Find top-K matching chunks via FAISS similarity search
4. **Answer Synthesis**: Augment LLM with context to generate final response

### AWS Infrastructure

![RAG system aws components architecture](/images/projects/project-serverlessrag/aws_architecture.png)

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **Vector Database**: FAISS
- **Cloud Platform**: AWS (EC2, S3, VPC, ALB)
- **Embeddings**: Amazon Titan models
- **LLM Integration**: Support for GPT and Claude

## 📦 Installation & Deployment

### Prerequisites

- AWS Account with IAM permissions
- Docker installed
- Python 3.11+

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/Wiran-Larbi/serverless-rag.git
cd serverless-rag

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run services locally
streamlit run admin.py
streamlit run client.py
```

### AWS Deployment

```bash
# Build the Docker images
docker build -t rag-admin:latest -f admin.Dockerfile .
docker build -t rag-client:latest -f client.Dockerfile .

# Run the containers
docker run -d \
  --name rag-admin \
  -p 8083:8083 \
  --restart unless-stopped \
  rag-admin:latest

docker run -d \
  --name rag-client \
  -p 8084:8084 \
  --restart unless-stopped \
  rag-client:latest
```

## 🔐 Security & Configuration

The system uses the following security measures:
- HTTPS endpoints
- IAM Role authentication for admin access
- API Key/Bearer authentication for client access
- VPC isolation for internal services

### VPC Configuration

```yaml
VPC:
  PublicSubnets:
    - CIDR: 10.0.1.0/24
      AZ: us-east-1a
  PrivateSubnets:
    - CIDR: 10.0.2.0/24
      AZ: us-east-1b
    - CIDR: 10.0.3.0/24
      AZ: us-east-1c
  SecurityGroups:
    ALB-SG:
      Ingress:
        - Protocol: TCP
          Ports: [80, 443]
    EC2-SG:
      Ingress:
        - Protocol: TCP
          Ports: [8083-8084]
          Source: ALB-SG
```

## 📚 Usage

### Admin Interface
Access the admin interface to upload and manage documents:
```
https://api.example.com/admin
```

### Client Interface
Access the client interface to query documents:
```
https://api.example.com/client
```

### API Access
The system exposes REST APIs for programmatic access. See the [API Documentation](docs/api.md).

## 📝 FAQ

**Q: How is FAISS storage synchronized between instances?**  
A: We use an S3-backed synchronization layer that:
1. Maintains a primary FAISS index in us-east-1
2. Replicates to read-only replicas in other regions
3. Uses versioned S3 objects for consistency

> **Important:** Ensure proper VPC peering configuration when accessing from other AWS services!

**Q: What document formats are supported?**  
A: Currently we support PDF documents, with plans to add DOCX, TXT, and HTML in future releases.

**Q: Can I customize the embedding models?**  
A: Yes, the system is designed to work with custom embedding models. See the configuration guide.

## 📊 Performance

The system is designed to handle:
- Up to 10,000 pages of documents
- Response times < 2 seconds for most queries
- Concurrent users: up to 50 simultaneous queries

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Wiran Larbi - [@WiranLarbi](https://twitter.com/WiranLarbi) - wiran.larbi@example.com

Project Link: [https://github.com/Wiran-Larbi/serverless-rag](https://github.com/Wiran-Larbi/serverless-rag)
