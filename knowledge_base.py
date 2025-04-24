import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai

def create_knowledge_base(custom_pdf_path=None, custom_text=None):
    """
    Create a knowledge base from insurance policy documents or custom text.
    
    Args:
        custom_pdf_path: Path to a custom PDF document
        custom_text: Custom text to use instead of documents
        
    Returns:
        A vector store containing insurance policy information
    """
    # Set up Google API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Load the documents
    documents = []
    
    if custom_text:
        # Create a temporary file for the custom text
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w+') as tmp_file:
            tmp_file.write(custom_text)
            tmp_path = tmp_file.name
        
        # Load the text file
        loader = TextLoader(tmp_path)
        documents = loader.load()
        
        # Clean up the temporary file
        os.unlink(tmp_path)
        
    elif custom_pdf_path:
        # Load the custom PDF file
        loader = PyPDFLoader(custom_pdf_path)
        documents = loader.load()
        
    else:
        # Load default insurance policy documents from sample_insurance_policies directory
        # If the directory doesn't exist, create it
        directory_path = "sample_insurance_policies"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            create_sample_insurance_files(directory_path)
            
        # Load all PDFs from the directory
        try:
            from glob import glob
            pdf_files = glob(f"{directory_path}/*.pdf")
            
            if not pdf_files:
                create_sample_insurance_files(directory_path)
                pdf_files = glob(f"{directory_path}/*.pdf")
            
            for pdf_file in pdf_files:
                loader = PyPDFLoader(pdf_file)
                documents.extend(loader.load())
                
        except Exception as e:
            print(f"Error loading default documents: {str(e)}")
            # Create a simple text document as fallback
            documents = [create_fallback_document()]
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings with Google Generative AI
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Create FAISS vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    print(f"Created knowledge base with {len(chunks)} chunks")
    return vector_store

def create_sample_insurance_files(directory_path):
    """
    Create sample insurance policy text files in the specified directory.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    # Sample insurance policy content
    policies = {
        "auto_insurance.pdf": """
        AUTO INSURANCE POLICY
        
        COVERAGE OPTIONS:
        - Liability coverage: Covers bodily injury and property damage to others
        - Collision coverage: Covers damage to your vehicle from an accident
        - Comprehensive coverage: Covers damage from theft, vandalism, or natural disasters
        - Personal injury protection: Covers medical expenses regardless of fault
        - Uninsured/underinsured motorist: Covers damages caused by drivers with insufficient insurance
        
        PREMIUM FACTORS:
        - Driving history and experience
        - Vehicle make, model, and year
        - Location and usage
        - Credit score (in some states)
        - Annual mileage
        
        CLAIM PROCESS:
        1. Report the accident immediately to your insurance company
        2. Provide necessary documentation (police report, photos)
        3. Insurance adjuster assesses the damage
        4. Receive and review the settlement offer
        5. Accept payment or negotiate further
        
        DISCOUNTS:
        - Safe driver discount
        - Multi-policy discount
        - Good student discount
        - Anti-theft device discount
        - Defensive driving course completion
        """,
        
        "health_insurance.pdf": """
        HEALTH INSURANCE POLICY
        
        PLAN TYPES:
        - HMO (Health Maintenance Organization): Lower costs, limited network
        - PPO (Preferred Provider Organization): More flexibility, higher premiums
        - HDHP (High Deductible Health Plan): Lower premiums, higher out-of-pocket costs
        - EPO (Exclusive Provider Organization): No out-of-network coverage except emergencies
        
        COVERED SERVICES:
        - Preventive care (annual check-ups, vaccinations)
        - Emergency services
        - Hospitalization
        - Prescription drugs
        - Mental health services
        - Maternity and newborn care
        
        COST SHARING:
        - Premium: Monthly payment to maintain coverage
        - Deductible: Amount paid before insurance begins coverage
        - Copayment: Fixed amount paid for specific services
        - Coinsurance: Percentage of costs paid after meeting deductible
        - Out-of-pocket maximum: Limit on total annual expenses
        
        ENROLLMENT PERIODS:
        - Open Enrollment: Annual period to enroll or change plans
        - Special Enrollment: Available after qualifying life events
        """,
        
        "home_insurance.pdf": """
        HOME INSURANCE POLICY
        
        COVERAGE COMPONENTS:
        - Dwelling coverage: Structure of your home
        - Personal property: Belongings inside your home
        - Liability protection: Legal expenses if someone is injured on your property
        - Additional living expenses: Temporary housing if your home is uninhabitable
        - Other structures: Detached garage, sheds, fences
        
        POLICY TYPES:
        - HO-1: Basic form (limited perils)
        - HO-2: Broad form (named perils)
        - HO-3: Special form (open perils for dwelling, named perils for contents)
        - HO-5: Comprehensive form (open perils for both dwelling and contents)
        - HO-6: Condo insurance
        - HO-8: Older home insurance
        
        CLAIM PROCESS:
        1. Document damage with photos/videos
        2. Contact your insurance company promptly
        3. Complete claim forms
        4. Meet with insurance adjuster
        5. Obtain repair estimates
        6. Receive and review settlement offer
        
        DISCOUNTS:
        - Home security systems
        - Smoke detectors and fire alarms
        - Impact-resistant roof
        - Bundling with auto insurance
        - Claims-free history
        """,
        
        "life_insurance.pdf": """
        LIFE INSURANCE POLICY
        
        POLICY TYPES:
        - Term life: Coverage for specified period (10, 20, 30 years)
        - Whole life: Lifetime coverage with cash value component
        - Universal life: Flexible premiums and death benefits
        - Variable life: Investment component with market-based returns
        
        DETERMINING FACTORS:
        - Age and gender
        - Health status and medical history
        - Family medical history
        - Lifestyle (smoking, high-risk activities)
        - Occupation
        - Driving record
        
        BENEFITS:
        - Death benefit: Tax-free payment to beneficiaries
        - Cash value (permanent policies): Grows tax-deferred
        - Accelerated benefits: Early access for terminal illness
        - Riders: Additional coverage options (disability, critical illness)
        
        APPLICATION PROCESS:
        1. Choose policy type and coverage amount
        2. Complete application
        3. Medical examination (may be waived for simplified issue policies)
        4. Underwriting review
        5. Policy approval and delivery
        6. Regular premium payments
        
        TAX ADVANTAGES:
        - Tax-free death benefits
        - Tax-deferred cash value growth
        - Potential for tax-free policy loans
        """
    }
    
    # Create each sample PDF file
    for filename, content in policies.items():
        file_path = os.path.join(directory_path, filename)
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        
        # Split content into lines and write to PDF
        y_position = height - 40
        c.setFont("Helvetica", 12)
        
        for line in content.split('\n'):
            if y_position < 40:
                c.showPage()  # Start a new page
                y_position = height - 40
            
            c.drawString(40, y_position, line.strip())
            y_position -= 14
        
        c.save()
        print(f"Created sample file: {file_path}")

def create_fallback_document():
    """Create a fallback document in case sample files cannot be generated."""
    from langchain_core.documents import Document
    
    content = """
    INSURANCE POLICIES OVERVIEW
    
    AUTO INSURANCE:
    Coverage for vehicle damage and liability for accidents. Includes collision, comprehensive, 
    and liability coverage. Premiums based on driving history, vehicle type, and location.
    
    HEALTH INSURANCE:
    Coverage for medical expenses. Plan types include HMO, PPO, and HDHP. 
    Costs include premiums, deductibles, copays, and coinsurance.
    
    HOME INSURANCE:
    Protection for your home and belongings. Covers dwelling, personal property,
    liability, and additional living expenses. Premiums based on home value and location.
    
    LIFE INSURANCE:
    Financial protection for beneficiaries after death. Types include term life,
    whole life, and universal life. Premiums based on age, health, and coverage amount.
    """
    
    return Document(page_content=content)