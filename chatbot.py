from flask import Flask, request, jsonify, render_template
import PyPDF2
import faiss
import numpy as np
from openai import OpenAI

# ---------------- APP SETUP ----------------
app = Flask(__name__)
client = OpenAI()

chunks = []
index = None

# ---------------- SMALL TALK ----------------
def handle_small_talk(user_input):
    text = user_input.lower().strip()

    greetings = [
        "hi", "hello", "hey",
        "good morning", "good afternoon", "good evening"
    ]

    closing = [
        "bye", "thank you", "thanks",
        "ok thank you", "ok thanks", "that's all"
    ]

    for i in greetings:
        if i==text or text.startswith(i):
            return "Hi 👋 How can I help you?"

    for j in closing:
        if j in text:
            return "You're welcome 😊 Feel free to ask anytime. Goodbye 👋"

    return None 

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- PDF UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload_pdf():
    global chunks, index

    pdf = request.files["pdf"]
    if not pdf or not pdf.filename.endswith(".pdf"):
        return jsonify({"message": "❌ Please upload a valid PDF file"}), 400

    reader = PyPDF2.PdfReader(pdf)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    if not text.strip():
        return jsonify({"message": "❌ No readable text found in PDF"}), 400

    chunks = make_chunks(text)
    embeddings = get_embeddings(chunks)
    index = build_faiss_index(embeddings)

    return jsonify({"message": "✅ PDF processed successfully!"})

     

def make_chunks(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size- overlap 
    return chunks

def get_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-3-small"
        )
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings).astype("float32") 

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1] 
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)
    return faiss_index


# ---------------- ASK QUESTION ----------------
@app.route("/ask", methods=["POST"])
def ask():
    global chunks, index

    question = request.json["question"]

    small_talk_response = handle_small_talk(question)
    if small_talk_response:
        return jsonify({"answer": small_talk_response})


    if index is None:
        return jsonify({"answer": "❌ Please upload a PDF first."})


    q_embed = client.embeddings.create(input=question,model="text-embedding-3-small").data[0].embedding
    q_embed = np.array([q_embed]).astype("float32")

    distances, indices = index.search(q_embed, 3)
    if distances[0][0] > 1.4:
        return jsonify({"answer": "❌ Please ask a valid question related to the document."})
    
    context = "\n\n".join([chunks[i] for i in indices[0]])
    prompt = f"""
Answer the question using ONLY the context below.
Context:
{context}
Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"answer": response.choices[0].message.content})

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
