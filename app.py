import streamlit as st
import fitz
import os
import re
import uuid
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv


# Ortam değişkenlerini yükle
#load_dotenv()
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Streamlit sayfa ayarları
st.set_page_config(page_title="TSK İç Hizmet Asistanı", layout="wide")
st.title("⚖️ TSK İç Hizmet Asistanı")


form_key = f"chat_form_{uuid.uuid4()}"  # Her yüklemede benzersiz form anahtarı
# Stil (sayfayı ortala ve daha güzel UI için padding)
st.markdown("""
            
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 800px;
        margin: auto;
    }
    .chat-bubble {
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .user {
        background-color: #e0f7fa;
        text-align: right;
    }
    .assistant {
        background-color: #f1f8e9;
        text-align: left;
    }
    .custom-input {
        max-width: 700px;
        margin: 2rem auto 1rem auto;
    }
</style>
""", unsafe_allow_html=True)

# PDF satırlarını yükleyen fonksiyon
@st.cache_data
def load_pdf_lines(path):
    doc = fitz.open(path)
    lines = []
    for page_num, page in enumerate(doc):
        for line in page.get_text().split('\n'):
            if line.strip():
                lines.append(Document(page_content=line.strip(), metadata={"page": page_num + 1}))
    return lines

# FAISS vektör veritabanını oluşturan veya yükleyen fonksiyon
@st.cache_resource
def create_vectorstore():
    vectorstore_path = "vectorstore"
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    if os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
        return FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    else:
        all_docs = []
        pdf_folder = os.path.join(os.getcwd(), 'tsk_mevzuat_dosyalari')
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, filename)
                docs = load_pdf_lines(pdf_path)
                for doc in docs:
                    doc.metadata["file"] = filename  # hangi PDF'ten geldiğini metadata'ya ekle
                all_docs.extend(docs)

        vectorstore = FAISS.from_documents(all_docs, embeddings)
        vectorstore.save_local(vectorstore_path)
        return vectorstore
    
# Markdown cevabı biçimlendir
def format_markdown_answer(text):
    text = re.sub(r"📘 (.*?)(?=\n|$)", r"**📘 \1**", text)
    text = re.sub(r"📜 (.*?)(?=\n|$)", r"**📜 \1**", text)
    text = re.sub(r"📌 (.*?)(?=\n|$)", r"**📌 \1**", text)
    text = re.sub(r"🧠 (.*?)(?=\n|$)", r"**🧠 \1**", text)
    return text

# Madde numarasını çıkart
def extract_article_number(text):
    match = re.search(r"(?i)(madde|md\.)\s*(\d+)", text)
    return match.group(0) if match else "–"

# Chat Prompt Template
system_prompt = """
Sen, Türk Silahlı Kuvvetleri personeline yönelik hazırlanmış uzman bir askeri hukuk asistanısın.
Görevin, aşağıdaki mevzuatlar hakkında doğru, açık, sade ve gerektiğinde yorum içeren bilgiler vermektir:

- 211 sayılı TSK İç Hizmet Kanunu

Kurallar:
1. Kullanıcı tüm bu metinlere muhataptır, her biri senin kapsama alanındadır.
2. Cevap verirken şu sırayı uygula:
   - 📘 Hangi mevzuat ve maddeyle ilgili olduğunu belirt (mümkünse madde numarası).
   - 📜 Hükmü özetle veya doğrudan aktar.
   - 📌 “Özet / Açıklama:” başlığı altında sadeleştir.
3. Eğer kullanıcı açıkça yorum isterse (“yorumla”, “fikir yürüt”, “sence” vs. gibi ifadelerle), ayrıca:
   - 🧠 “Yorum (resmî hüküm değildir):” başlığıyla dikkatli yorum ekle.
   - Yorumda bağlayıcılık olmadığını belirt.
4. Mevzuatta doğrudan bir hüküm yoksa bunu dürüstçe açıkla. Varsa kıyasla yaklaşım kullan.
5. Dilin sade ama hukuken doğru olmalı. Spekülatif ifadelerden kaçın.

Amacın: Kullanıcının bu dört mevzuata dair net, açık ve gerektiğinde yorumlu bilgiye ulaşmasını sağlamaktır.

Relevant documents: {context}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}"),
])


# Gemini RAG zinciri oluşturma
@st.cache_resource
def build_chain(_vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=GOOGLE_API_KEY)
    retriever = _vectorstore.as_retriever(search_kwargs={"k": 10})
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True, chain_type="stuff", chain_type_kwargs={"prompt": prompt})



# Veritabanını hazırla
with st.spinner("🔄 FAISS vektör veritabanı hazırlanıyor..."):
    vector_db = create_vectorstore()
    rag_chain = build_chain(_vectorstore=vector_db)


# --- Zincir Hazırla ---
with st.spinner("🔄 Mevzuat vektör veritabanı hazırlanıyor..."):
    vector_db = create_vectorstore()
    rag_chain = build_chain(vector_db)

# --- Sorgu Kutusu ---
with st.form(key="chat_form"):
    query = st.text_input("💬 Mevzuata dair bir soru yazın:", key="input_text")

    col1, col2 = st.columns([3, 1])  # Yanıtla ve Sil butonlarını yan yana koy
    with col1:
        submit = st.form_submit_button("✅ Yanıtla")
    with col2:
        clear = st.form_submit_button("🗑️ Temizle")

# --- İşlemler ---
if clear:
    st.session_state.chat_history = []

if submit and query:
    with st.spinner("🔍 Yanıt hazırlanıyor..."):
        result = rag_chain(query)

        # Kullanıcı mesajı
        st.markdown(f"""
        <div class="chat-bubble user">
            👤 <strong>Siz:</strong><br>{query}
        </div>
        """, unsafe_allow_html=True)

        # Asistan cevabı
        formatted_answer = format_markdown_answer(result['result'])
        st.markdown(f"""
        <div class="chat-bubble assistant">
            🤖 <strong>Asistan:</strong><br>{formatted_answer}
        </div>
        """, unsafe_allow_html=True)
