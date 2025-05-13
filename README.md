
## Table of Contents
- [Features](#-features)
- [Prerequisites](#-Prerequisites)
- [Setup_Instructions](#-SetupInstructions)
- [Running_the_application](#-Runningtheapplication)
- [Trouble_shooting](#-Troubleshooting)
- [License](#-license)
#  PDF Chatbot with Groq and LangChain
A conversational AI application that allows you to chat with multiple PDF documents using Groq's lightning-fast LLMs and Hugging Face embeddings.


## Features

- Upload and process multiple PDF files
-  Natural language questioning about document contents

- Fast responses powered by Groq's inference engine
- State-of-the-art embeddings from Hugging Face


## Prerequisites

- Python 3.8+
- Groq API key
- Basic understanding of LangChain and Streamlit
## Setup Instructions

### 1. Obtain API Keys

#### Groq API Key
1. Go to [Groq's Cloud Console](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to the "API Keys" section
4. Click "Create API Key" and copy the generated key
5. For model documentation, see: [Llama3-8b-8192 Docs](https://console.groq.com/docs/model/llama3-8b-8192)

#### Hugging Face Embeddings
The application uses the `BAAI/bge-large-en-v1.5` embedding model:
- Model Card: [BAAI/bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5)
- No API key required (model is downloaded automatically)
#### When to Use Which
- Use Local Download if:

  - You have the disk/memory resources.

  - Privacy/offline operation matters.

  - You’ll make many embeddings (no API costs).

- Use API if:

  - You cannot run large models locally (e.g., on a small cloud instance).

  - You need embeddings infrequently.

#### Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pdf-chatbot.git
   
   cd pdf-chatbot
   ```

2.  Create a virtual environment
  ```bash
  python -m venv venv

  source venv/bin/activate 

# On Windows use `venv\Scripts\activate`
```

3. Install dependencies
  ```bash
 pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Groq API key
  ```bash
GROQ_API_KEY=your_api_key_here
```


5. The default embedding model doesn't require an API key. If you want to use other models or the model used in the orginal 
  -  Get token from Hugging Face Settings
  - Add to .env:
  ```bash
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

## Running the application 

Start the Streamlit application:
```bash
streamlit run app.py
```

## 🖥️ Usage

1.Upload one or more PDF files using the sidebar

2.Click the "Process" button to ingest the documents

3.Once processing is complete, ask questions about the documents in the chat interface

4.The chatbot will provide answers based on the content of your PDFs##  ⚙️ Configuration Options
You can modify these parameters in the code:

![Image](https://github.com/user-attachments/assets/62b9b17b-6ec9-4abf-8ebe-e279693709b3)

### Groq LLM Settings (in groq_wrapper.py)
- model_name: Change to other supported Groq models (e.g., "mixtral-8x7b-32768")

- temperature: Adjust creativity (0.0-1.0)

- max_tokens: Control response length

### Text Processing (in app.py)
- chunk_size: Adjust document chunk size (default: 1000)

- chunk_overlap: Set overlap between chunks (default: 200)

- embedding_model: Change to other Hugging Face models if needed
## technical architecture
``` bash 
PDF Documents → Text Extraction → Chunking → Embedding → Vector Store
       ↑                                         ↓
User Questions ← Conversation Chain ← Retrieval ←─┘
```
## 🛠️ Trouble shooting 
### 1. API Key Not Found:

Ensure your .env file is in the root directory

Verify the key name matches GROQ_API_KEY

Restart the application after adding the key

### 2.PDF Text Extraction Problems:

Some PDFs with complex layouts may not extract perfectly

Try different PDF readers if needed

### 3.Model Loading Issues:

The embedding model will download on first run (≈1.3GB) Ensure you have stable internet connection

Or if your api key of the HuggingFace is correct 

## 📜 License
MIT License. See LICENSE for details.
