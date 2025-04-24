import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import streamlit as st

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # If API key is not set, warn but continue for development purposes
    print("Warning: GOOGLE_API_KEY not set in environment variables")

def load_documents(directory_path):
    """
    Load PDF documents from a directory.
    
    Args:
        directory_path (str): Path to the directory containing PDF documents
        
    Returns:
        list: List of loaded documents
    """
    try:
        # Check if directory exists
        if not os.path.exists(directory_path):
            st.warning(f"Directory '{directory_path}' does not exist. Creating sample files.")
            os.makedirs(directory_path, exist_ok=True)
            create_sample_pdf_content(directory_path)
        
        # Use DirectoryLoader to load all PDFs in the directory
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        
        documents = loader.load()
        print(f"Loaded {len(documents)} document pages from {directory_path}")
        
        # Log document metadata for debugging
        for i, doc in enumerate(documents[:3]):  # Log first 3 docs
            print(f"Document {i} metadata: {doc.metadata}")
            print(f"Document {i} content sample: {doc.page_content[:100]}...")
        
        return documents
    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        st.error(f"Error loading documents: {str(e)}")
        return []

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunks for processing.
    
    Args:
        documents (list): List of documents to split
        chunk_size (int): Size of each text chunk
        chunk_overlap (int): Overlap between chunks
        
    Returns:
        list: List of text chunks
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks")
        
        # Preserve metadata when splitting
        for i, chunk in enumerate(chunks):
            if 'source' not in chunk.metadata and 'source' in documents[0].metadata:
                chunk.metadata['source'] = documents[0].metadata['source']
        
        return chunks
    except Exception as e:
        print(f"Error splitting documents: {str(e)}")
        st.error(f"Error splitting documents: {str(e)}")
        return []

def create_vector_store(documents):
    """
    Create a FAISS vector store from documents.
    
    Args:
        documents (list): List of documents to embed
        
    Returns:
        FAISS: FAISS vector store with embedded documents
    """
    try:
        # Split documents into chunks
        chunks = split_documents(documents)
        if not chunks:
            return None
        
        # Create embeddings using Google Generative AI
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Create FAISS vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        print("Created FAISS vector store successfully")
        
        # Log vector store info
        print(f"Vector store contains {len(chunks)} chunks")
        
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {str(e)}")
        st.error(f"Error creating vector store: {str(e)}")
        return None

def create_sample_pdf_content(directory_path):
    """
    Create sample PDF files with insurance policy information.
    This is only used when no PDF files are available in the specified directory.
    
    Args:
        directory_path (str): Directory to create sample files in
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Sample content for different insurance policies
        sample_policies = {
            "auto_insurance.pdf": """
            AUTO INSURANCE POLICY
            
            COVERAGE OPTIONS:
            - Liability coverage: Covers bodily injury and property damage to others
            - Collision coverage: Covers damage to your vehicle from an accident
            - Comprehensive coverage: Covers damage to your vehicle from non-collision events
            - Personal injury protection: Covers medical expenses regardless of fault
            - Uninsured/underinsured motorist coverage: Protects you if the other driver has insufficient insurance
            
            PREMIUM FACTORS:
            - Driving history
            - Vehicle type and age
            - Annual mileage
            - Credit score
            - Location
            - Age and driving experience
            
            CLAIMS PROCESS:
            1. Report the accident to your insurance company immediately
            2. Provide all necessary documentation (police report, photos, etc.)
            3. An adjuster will assess the damage
            4. Review the settlement offer
            5. Receive payment for covered damages
            
            DISCOUNTS AVAILABLE:
            - Safe driver discount
            - Multi-policy discount
            - Good student discount
            - Anti-theft device discount
            - Defensive driving course discount
            """,
            
            "health_insurance.pdf": """
            HEALTH INSURANCE POLICY
            
            COVERAGE OPTIONS:
            - HMO (Health Maintenance Organization): Lower cost but limited provider network
            - PPO (Preferred Provider Organization): More flexibility in choosing providers
            - High-deductible health plans: Lower premiums but higher out-of-pocket costs
            - Medicare Advantage: For seniors and those with disabilities
            - Medicaid: For low-income individuals and families
            
            COVERED SERVICES:
            - Preventive care
            - Emergency services
            - Hospitalization
            - Prescription drugs
            - Mental health services
            - Maternity and newborn care
            
            PREMIUM FACTORS:
            - Age
            - Location
            - Family size
            - Tobacco use
            - Plan category
            
            CLAIMS PROCESS:
            1. Visit in-network provider
            2. Provider submits claim to insurance
            3. Insurance processes claim
            4. Patient receives explanation of benefits
            5. Patient pays remaining balance after insurance coverage
            
            ENROLLMENT PERIODS:
            - Open enrollment period: Annual period to enroll or change plans
            - Special enrollment period: After qualifying life events
            """,
            
            "home_insurance.pdf": """
            HOME INSURANCE POLICY
            
            COVERAGE OPTIONS:
            - Dwelling coverage: Protects the structure of your home
            - Personal property coverage: Covers belongings inside your home
            - Liability protection: Covers legal expenses if someone is injured on your property
            - Additional living expenses: Covers costs if you cannot live in your home due to covered damage
            
            PREMIUM FACTORS:
            - Home value and age
            - Location and proximity to fire station
            - Construction materials
            - Security features
            - Previous claims
            - Credit score
            
            CLAIMS PROCESS:
            1. Document damage with photos and videos
            2. Contact your insurance company immediately
            3. Complete claim forms
            4. Meet with the insurance adjuster
            5. Receive payment for covered damages
            6. Complete repairs
            
            DISCOUNTS AVAILABLE:
            - Bundle with auto insurance
            - Security system discount
            - Fire protection discount
            - New home discount
            - Loyalty discount
            """,
            
            "life_insurance.pdf": """
            LIFE INSURANCE POLICY
            
            TYPES OF POLICIES:
            - Term life insurance: Coverage for a specific period
            - Whole life insurance: Lifetime coverage with cash value
            - Universal life insurance: Flexible premiums and death benefits
            - Variable life insurance: Investment component with variable returns
            
            PREMIUM FACTORS:
            - Age and gender
            - Health status
            - Family medical history
            - Lifestyle choices (smoking, high-risk activities)
            - Occupation
            - Coverage amount
            
            DEATH BENEFIT PAYOUT:
            1. Beneficiary submits death certificate and claim form
            2. Insurance company verifies the claim
            3. Death benefit is paid to beneficiaries
            4. Beneficiaries can choose lump sum or installment payments
            
            TAX BENEFITS:
            - Death benefits are generally income tax-free to beneficiaries
            - Cash value grows tax-deferred
            - Certain premium payments may be tax-deductible for business owners
            
            POLICY RIDERS:
            - Accidental death benefit
            - Waiver of premium
            - Critical illness rider
            - Long-term care rider
            """
        }
        
        # Create each sample PDF file
        for filename, content in sample_policies.items():
            file_path = os.path.join(directory_path, filename)
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            
            # Split content into lines and write to PDF
            y_position = height - 40
            c.setFont("Helvetica", 12)
            
            for line in content.split('\n'):
                if y_position < 40:
                    c.showPage()
                    y_position = height - 40
                
                c.drawString(40, y_position, line.strip())
                y_position -= 14
            
            c.save()
            print(f"Created sample file: {file_path}")
        
    except Exception as e:
        print(f"Error creating sample PDF files: {str(e)}")
        st.error(f"Error creating sample PDF files: {str(e)}")
