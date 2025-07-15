#pip install PyPDF2 transformers tf-keras tensorflow sentence-transformers faiss-cpu google-genereativeai python-docx 

import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
from docx import Document

GOOGLE_API_KEY = ''
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text(file_path):
    text = ""
    try:
        if file_path.lower().endswith('.pdf'):
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() or ""
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        else:
            return "Error: Unsupported file type. Please provide a .pdf and .docx file."
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    chunks = []
    words = text.split()
    for i in range(0, len(words) - chunk_size, chunk_size - chunk_overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    chunks.append(" ".join(words[len(words) - chunk_size:]))
    return chunks

def retrieve_relevant_chunks(query, index, embedding_model, chunks, top_k=3):
    query_embedding = embedding_model.encode([query])
    _, top_indices = index.search(query_embedding, top_k)
    relevant_chunks = [chunks[i] for i in top_indices[0]]
    return relevant_chunks

file_path = "AI.docx"  # Replace with your PDF path
full_text = extract_text(file_path)
chunks = chunk_text(full_text)

# Embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedding_model.encode(chunks)

# Vector Search Index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
def summarize_with_gemini(text):
    """Summarizes the given text using the Gemini API."""

    model = genai.GenerativeModel('gemini-2.0-flash')  # Or the appropriate model
    prompt = f"Summarize the following text:\n{text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return "Error: Could not generate summary."
    
# Summarization
query = "Summarize the key concepts of AI and its applications"
relevant_chunks = retrieve_relevant_chunks(query, index, embedding_model, chunks)
context = " ".join(relevant_chunks)
# Generate summary using Gemini API
final_summary = summarize_with_gemini(context)
print("Summary using Gemini API:", final_summary)