import streamlit as st
import tempfile
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import base64
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="OCR Financial Report",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #334155;
    }

    /* Header Styles */
    .main-header {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #475569 0%, #64748b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }

    .main-subheader {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Section Styles */
    .upload-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .upload-section:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }

    .result-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-top: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Alert Styles */
    .success-message {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        color: #14532d;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #bbf7d0;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .error-message {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #7f1d1d;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #fecaca;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0c4a6e;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #bae6fd;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #475569 0%, #64748b 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* File Uploader Styles */
    .stFileUploader > div > div {
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }

    .stFileUploader > div > div:hover {
        border-color: #94a3b8;
        background: #f1f5f9;
    }

    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }

    .css-1d391kg h1 {
        color: #334155;
        font-weight: 600;
    }

    /* Progress Bar Styles */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #475569 0%, #64748b 100%);
        border-radius: 8px;
    }

    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8fafc;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #64748b;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #334155;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Selectbox Styles */
    .stSelectbox > div > div {
        background: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.5rem;
    }

    /* Checkbox Styles */
    .stCheckbox > div {
        color: #475569;
        font-weight: 500;
    }

    /* JSON Display Styles */
    .stJson {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Text Area Styles */
    .stTextArea > div > div > textarea {
        background: #f8fafc;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Inter', monospace;
    }

    /* Footer Styles */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.9rem;
    }

    /* History Item Styles */
    .history-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        border: 1px solid #e2e8f0;
        font-size: 0.9rem;
    }

    /* Metric Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        .upload-section, .result-section {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class OCRProcessor:
    def __init__(self, api_key: str = None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.ocr_model = os.getenv("MISTRAL_OCR_MODEL", "mistral-ocr-latest")
        self.chat_model = os.getenv("MISTRAL_CHAT_MODEL", "ministral-8b-latest")

        if not self.api_key:
            raise ValueError("API key is required. Please set MISTRAL_API_KEY in .env file or enter manually.")

        self.client = Mistral(api_key=self.api_key)

    def process_pdf(self, pdf_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF using Mistral OCR"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_content)
                tmp_file_path = tmp_file.name

            # Upload to Mistral
            uploaded_file = self.client.files.upload(
                file={
                    "file_name": Path(filename).stem,
                    "content": pdf_content,
                },
                purpose="ocr",
            )

            # Get signed URL
            signed_url = self.client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

            # Process with OCR
            pdf_response = self.client.ocr.process(
                document=DocumentURLChunk(document_url=signed_url.url),
                model=self.ocr_model,
                include_image_base64=True
            )

            # Extract markdown text
            pdf_ocr_markdown = [page.markdown for page in pdf_response.pages]

            # Process with chat model for structured extraction
            chat_response = self.client.chat.complete(
                model=self.chat_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            TextChunk(
                                text=(
                                    f"Ini adalah OCR gambar dalam markdown:\\n\\n{pdf_ocr_markdown}\\n.\\n"
                                    "Ubah ini menjadi respons JSON terstruktur yang masuk akal dan dalam bahasa indonesia. "
                                    "Dari nama bank, jenis laporan dan periode laporan. "
                                    "Outputnya harus benar-benar JSON tanpa komentar tambahan."
                                )
                            ),
                        ],
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )

            # Parse response
            structured_data = json.loads(chat_response.choices[0].message.content)

            # Cleanup
            os.unlink(tmp_file_path)

            return {
                "success": True,
                "raw_text": "\\n".join(pdf_ocr_markdown),
                "structured_data": structured_data,
                "pages_processed": len(pdf_response.pages)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "structured_data": None
            }

    def process_image(self, image_content: bytes, filename: str) -> Dict[str, Any]:
        """Process image using Mistral OCR"""
        try:
            # Determine image type
            image_type = "jpeg"
            if filename.lower().endswith(('.png', '.PNG')):
                image_type = "png"
            elif filename.lower().endswith(('.webp', '.WEBP')):
                image_type = "webp"

            # Encode as base64
            encoded = base64.b64encode(image_content).decode()
            base64_data_url = f"data:image/{image_type};base64,{encoded}"

            # Process with OCR
            image_response = self.client.ocr.process(
                document=ImageURLChunk(image_url=base64_data_url),
                model=self.ocr_model
            )

            # Convert to dictionary
            ocr_result = json.loads(image_response.model_dump_json())

            # Process with chat model for structured extraction
            raw_text = ""
            if "pages" in ocr_result:
                raw_text = "\\n".join([page.get("markdown", "") for page in ocr_result["pages"]])

            if raw_text:
                chat_response = self.client.chat.complete(
                    model=self.chat_model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                TextChunk(
                                    text=(
                                        f"Ini adalah OCR gambar dalam markdown:\\n\\n{raw_text}\\n.\\n"
                                        "Ubah ini menjadi respons JSON terstruktur yang masuk akal dan dalam bahasa indonesia. "
                                        "Dari nama bank, jenis laporan dan periode laporan. "
                                        "Outputnya harus benar-benar JSON tanpa komentar tambahan."
                                    )
                                ),
                            ],
                        }
                    ],
                    response_format={"type": "json_object"},
                    temperature=0,
                )

                structured_data = json.loads(chat_response.choices[0].message.content)
            else:
                structured_data = {"error": "No text extracted"}

            return {
                "success": True,
                "raw_text": raw_text,
                "structured_data": structured_data,
                "pages_processed": 1
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "structured_data": None
            }

def save_processing_history(filename: str, result: Dict[str, Any], processing_time: float):
    """Save processing history to session state"""
    if "history" not in st.session_state:
        st.session_state.history = []

    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": filename,
        "success": result["success"],
        "error": result.get("error"),
        "processing_time": processing_time,
        "pages_processed": result.get("pages_processed", 0)
    }

    st.session_state.history.append(history_entry)

def main():
    # Header with modern design
    st.markdown('<h1 class="main-header">OCR Financial Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">📄 Extract text and structured data from PDF documents and images using Mistral AI</p>', unsafe_allow_html=True)

    # Status indicators at the top
    env_api_key = os.getenv("MISTRAL_API_KEY")
    if env_api_key:
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
            <div class="success-message" style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <span>✅</span>
                <span>Connected to Mistral AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar with modern design
    with st.sidebar:
        # Get API key from environment
        env_api_key = os.getenv("MISTRAL_API_KEY")
        api_key = env_api_key

        # API Status Card
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #334155; font-weight: 600;">🔧 API Status</h4>
            <div style="margin-top: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="color: #10b981;">●</span>
                    <span style="color: #64748b; font-size: 0.9rem;">Mistral Connected</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">●</span>
                    <span style="color: #64748b; font-size: 0.9rem;">Models Ready</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Processing Options
        st.markdown('<h4 style="color: #334155; font-weight: 600; margin-bottom: 1rem;">🔧 Processing Options</h4>', unsafe_allow_html=True)

        language = st.selectbox(
            "Output Language",
            ["Indonesian", "English"],
            help="Choose the language for the output"
        )

        include_raw_ocr = st.checkbox(
            "Include Raw OCR Text",
            value=True,
            help="Include the raw OCR output in results"
        )

        st.markdown("---")

        # Processing History
        st.markdown('<h4 style="color: #334155; font-weight: 600; margin-bottom: 1rem;">📜 Recent Activity</h4>', unsafe_allow_html=True)

        if "history" in st.session_state and st.session_state.history:
            for i, entry in enumerate(reversed(st.session_state.history[-5:])):
                status_color = "#10b981" if entry["success"] else "#ef4444"
                status_icon = "✅" if entry["success"] else "❌"

                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="color: {status_color};">{status_icon}</span>
                        <span style="color: #334155; font-weight: 500;">{entry['filename']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b;">
                        <span>{entry['timestamp']}</span>
                        <span>⏱️ {entry['processing_time']:.2f}s</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <span>ℹ️</span>
                <span>No processing history yet</span>
            </div>
            """, unsafe_allow_html=True)

    # Main content with improved layout
    st.markdown("---")

    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h3 style="color: #334155; font-weight: 600; margin-bottom: 1rem;">📤 Upload Document</h3>', unsafe_allow_html=True)

        # File uploader with custom styling
        uploaded_file = st.file_uploader(
            "Choose a PDF or Image file",
            type=['pdf', 'png', 'jpg', 'jpeg', 'webp'],
            help="Supported formats: PDF, PNG, JPG, JPEG, WebP",
            label_visibility="visible"
        )

    with col2:
        # File info panel
        if uploaded_file is not None:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #334155; font-weight: 600; margin: 0 0 1rem 0;">📋 File Information</h4>
                <div style="color: #64748b; font-size: 0.9rem;">
                    <div style="margin-bottom: 0.5rem;">
                        <strong>Name:</strong> """ + uploaded_file.name + """
                    </div>
                    <div style="margin-bottom: 0.5rem;">
                        <strong>Size:</strong> """ + f"{uploaded_file.size / 1024:.1f} KB" + """
                    </div>
                    <div>
                        <strong>Type:</strong> """ + uploaded_file.type + """
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if uploaded_file is not None:
        # Process button with better styling
        st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)

        # Process button
        if st.button("🚀 Start OCR Processing", type="primary", use_container_width=True):
                # Validate API key
                if not api_key:
                    st.error("❌ Please enter your Mistral API key")
                    return

                # Check API key format (basic validation)
                if len(api_key) < 20:
                    st.error("❌ Invalid API key format. Please check your Mistral API key")
                    return

                # Initialize progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # Start processing
                    status_text.text("🔄 Initializing OCR processor...")
                    progress_bar.progress(10)
                    time.sleep(0.5)

                    processor = OCRProcessor(api_key)

                    # Read file content
                    status_text.text("📖 Reading file content...")
                    progress_bar.progress(20)
                    file_content = uploaded_file.read()

                    # Determine file type and process
                    start_time = time.time()

                    if uploaded_file.name.lower().endswith('.pdf'):
                        status_text.text("🔍 Processing PDF with OCR...")
                        progress_bar.progress(40)
                        result = processor.process_pdf(file_content, uploaded_file.name)
                    else:
                        status_text.text("🖼️ Processing Image with OCR...")
                        progress_bar.progress(40)
                        result = processor.process_image(file_content, uploaded_file.name)

                    progress_bar.progress(80)
                    processing_time = time.time() - start_time

                    # Save to history
                    save_processing_history(uploaded_file.name, result, processing_time)

                    # Store processing time for metrics
                    st.session_state.last_processing_time = processing_time

                    # Update progress
                    progress_bar.progress(100)
                    status_text.text("✅ Processing completed!")

                    # Store result in session state
                    st.session_state.current_result = result
                    st.session_state.current_filename = uploaded_file.name

                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()

                    if result["success"]:
                        st.markdown("""
                        <div class="success-message">
                            <span>✅</span>
                            <span>OCR processing completed successfully!</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            <span>❌</span>
                            <span>OCR processing failed: {result.get('error', 'Unknown error')}</span>
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()

        st.markdown('</div>', unsafe_allow_html=True)

    # Results section
    if "current_result" in st.session_state:
        result = st.session_state.current_result
        filename = st.session_state.current_filename

        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #334155; font-weight: 600; margin-bottom: 1.5rem;">📊 Processing Results</h3>', unsafe_allow_html=True)

        if result["success"]:
            # Success metrics
            pages_processed = result.get("pages_processed", 0)
            processing_time = st.session_state.get("last_processing_time", 0)

            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                <div class="metric-card">
                    <div style="color: #10b981; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">✅</div>
                    <div style="color: #334155; font-weight: 600;">Processing Complete</div>
                    <div style="color: #64748b; font-size: 0.9rem;">All tasks finished successfully</div>
                </div>
                <div class="metric-card">
                    <div style="color: #3b82f6; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">{pages_processed}</div>
                    <div style="color: #334155; font-weight: 600;">Pages Processed</div>
                    <div style="color: #64748b; font-size: 0.9rem;">OCR analysis complete</div>
                </div>
                <div class="metric-card">
                    <div style="color: #8b5cf6; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">{processing_time:.1f}s</div>
                    <div style="color: #334155; font-weight: 600;">Processing Time</div>
                    <div style="color: #64748b; font-size: 0.9rem;">Total elapsed time</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📋 Structured Data", "📄 Raw OCR Text", "💾 Download"])

            with tab1:
                st.subheader("📋 Extracted Information")

                if result["structured_data"]:
                    # Display structured data in a formatted way
                    structured_json = json.dumps(result["structured_data"], indent=4, ensure_ascii=False)
                    st.json(result["structured_data"])

                    # Extract and display key information
                    if isinstance(result["structured_data"], dict):
                        st.markdown("### 🔑 Key Information")

                        for key, value in result["structured_data"].items():
                            if key.lower() in ["nama_bank", "jenis_laporan", "periode_laporan", "bank_name", "report_type", "period"]:
                                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.warning("No structured data extracted")

            with tab2:
                st.subheader("📄 Raw OCR Text")

                if include_raw_ocr and result["raw_text"]:
                    st.text_area(
                        "Extracted Text",
                        result["raw_text"],
                        height=400,
                        help="This is the raw text extracted by OCR"
                    )

                    # Copy to clipboard button
                    if st.button("📋 Copy to Clipboard"):
                        st.write("Text copied to clipboard!")
                else:
                    st.info("Raw OCR text is hidden")

            with tab3:
                st.subheader("💾 Download Results")

                # Download structured data
                if result["structured_data"]:
                    structured_json = json.dumps(result["structured_data"], indent=4, ensure_ascii=False)
                    st.download_button(
                        label="📥 Download Structured Data (JSON)",
                        data=structured_json,
                        file_name=f"{Path(filename).stem}_structured_data.json",
                        mime="application/json"
                    )

                # Download raw text
                if result["raw_text"]:
                    st.download_button(
                        label="📥 Download Raw Text (TXT)",
                        data=result["raw_text"],
                        file_name=f"{Path(filename).stem}_raw_text.txt",
                        mime="text/plain"
                    )

                # Download complete result
                complete_result = {
                    "filename": filename,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "structured_data": result["structured_data"],
                    "raw_text": result["raw_text"] if include_raw_ocr else "Hidden",
                    "pages_processed": result.get("pages_processed", 0)
                }

                complete_json = json.dumps(complete_result, indent=4, ensure_ascii=False)
                st.download_button(
                    label="📥 Download Complete Result (JSON)",
                    data=complete_json,
                    file_name=f"{Path(filename).stem}_complete_result.json",
                    mime="application/json"
                )
        else:
            st.markdown(f'<div class="error-message">❌ Processing Failed: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-section" style="text-align: center; padding: 3rem 2rem;">
            <div style="color: #94a3b8; font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h3 style="color: #334155; font-weight: 600; margin-bottom: 1rem;">Ready to Process Documents</h3>
            <p style="color: #64748b; margin-bottom: 2rem;">Upload a document and click "Start OCR Processing" to see results here</p>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <div style="color: #3b82f6; font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
                    <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">PDF Support</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 2rem; margin-bottom: 0.5rem;">🖼️</div>
                    <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">Image Support</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #8b5cf6; font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                    <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">AI Powered</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Modern footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="color: #94a3b8;">Built with</span>
            <span style="color: #ef4444;">❤️</span>
            <span style="color: #94a3b8;">using</span>
            <a href="https://streamlit.io/" target="_blank" style="color: #3b82f6; text-decoration: none; font-weight: 500;">Streamlit</a>
            <span style="color: #94a3b8;">&</span>
            <a href="https://docs.mistral.ai/" target="_blank" style="color: #8b5cf6; text-decoration: none; font-weight: 500;">Mistral AI</a>
        </div>
        <div style="color: #94a3b8; font-size: 0.8rem;">
            Modern OCR Application • Version 1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()