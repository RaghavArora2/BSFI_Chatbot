import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai
import logging
import io
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_knowledge_base(custom_pdf_path=None, custom_text=None):
    """
    Create a knowledge base from insurance policy documents or custom text.
    
    Args:
        custom_pdf_path: Path to a custom PDF document
        custom_text: Custom text to use instead of documents
        
    Returns:
        A vector store containing insurance policy information
    """
    documents = []
    
    # Use Google Generative AI for embeddings
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # Use a suitable embedding model
        google_api_key=api_key,
    )
    
    # Case 1: Use custom PDF if provided
    if custom_pdf_path:
        logger.info(f"Loading custom PDF from {custom_pdf_path}")
        loader = PyPDFLoader(custom_pdf_path)
        documents.extend(loader.load())
    
    # Case 2: Use custom text if provided
    elif custom_text:
        logger.info("Using custom text for knowledge base")
        # Create a temporary file to store the custom text
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
            temp_file.write(custom_text)
            temp_path = temp_file.name
        
        # Load the temporary text file
        loader = TextLoader(temp_path)
        documents.extend(loader.load())
        
        # Clean up temporary file
        os.unlink(temp_path)
    
    # Case 3: Use default sample insurance policy files (create them if needed)
    else:
        logger.info("Using default insurance policy documents")
        # Check if sample directory exists, if not create it
        sample_dir = "sample_insurance_policies"
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)
            # Create sample files
            create_sample_insurance_files(sample_dir)
        
        # Check for existing text files in attached_assets
        attached_dir = "attached_assets"
        if os.path.exists(attached_dir):
            for filename in os.listdir(attached_dir):
                if filename.endswith(".txt"):
                    file_path = os.path.join(attached_dir, filename)
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
                    logger.info(f"Loaded text file from {file_path}")
        
        # Load sample insurance policy files
        for policy_type in ["auto", "health", "home", "life"]:
            pdf_path = os.path.join(sample_dir, f"{policy_type}_insurance.pdf")
            if os.path.exists(pdf_path):
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
                logger.info(f"Loaded sample file from {pdf_path}")
    
    # If no documents are loaded, create a fallback document
    if not documents:
        logger.warning("No documents loaded, creating fallback document")
        fallback_text = create_fallback_document()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
            temp_file.write(fallback_text)
            temp_path = temp_file.name
        
        loader = TextLoader(temp_path)
        documents.extend(loader.load())
        
        # Clean up temporary file
        os.unlink(temp_path)
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created knowledge base with {len(chunks)} chunks")
    
    # Create and return vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


def create_sample_insurance_files(directory_path):
    """
    Create sample insurance policy text files in the specified directory.
    """
    try:
        import reportlab.pdfgen.canvas
        from reportlab.lib.pagesizes import letter

        # Sample content for different insurance policies
        insurance_data = {
            "auto_insurance": """
            AUTO INSURANCE POLICY
            COVERAGE TYPES:
            - Liability Coverage: Pays for bodily injury and property damage to others when you're at fault
            - Collision Coverage: Pays for damage to your vehicle from an accident
            - Comprehensive Coverage: Pays for damage from non-collision events (theft, weather, vandalism)
            - Personal Injury Protection (PIP): Covers medical expenses for you and passengers
            - Uninsured/Underinsured Motorist Coverage: Protects you from drivers with inadequate insurance
            
            POLICY LIMITS:
            - Per person/per accident limits (e.g., 100/300/50 = $100,000 per person, $300,000 per accident, $50,000 property damage)
            - Deductible: Amount you pay before insurance pays (typically $250, $500, or $1,000)
            
            FACTORS AFFECTING PREMIUMS:
            - Driving history and claims history
            - Vehicle type, age, and usage
            - Geographic location and garaging address
            - Credit score and age
            - Annual mileage
            
            FILING A CLAIM:
            1. Document the incident (photos, police report if applicable)
            2. Contact insurance company promptly
            3. Provide required information (policy number, date/time/location, other party's information)
            4. Work with assigned claims adjuster
            5. Get repair estimates
            
            DISCOUNTS:
            - Multi-policy discount
            - Good driver discount
            - Vehicle safety features
            - Good student discount
            - Defensive driving course
            """,
            "health_insurance": """
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
            "home_insurance": """
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
            "life_insurance": """
            LIFE INSURANCE POLICY
            TYPES OF POLICIES:
            - Term Life: Temporary coverage (10, 20, 30 years) with lower premiums
            - Whole Life: Permanent coverage with cash value component and fixed premiums
            - Universal Life: Permanent coverage with flexible premiums and investment options
            - Variable Life: Permanent coverage with investment options in sub-accounts
            
            POLICY COMPONENTS:
            - Death benefit: Amount paid to beneficiaries
            - Premium: Regular payment to maintain coverage
            - Cash value: Savings component in permanent policies
            - Riders: Additional coverage options (accelerated benefits, waiver of premium)
            
            ELIGIBILITY FACTORS:
            - Age and gender
            - Health condition and medical history
            - Family medical history
            - Lifestyle choices (smoking, high-risk activities)
            - Occupation
            
            APPLICATION PROCESS:
            1. Initial application
            2. Medical exam (can be waived for simplified issue policies)
            3. Medical underwriting (reviewing health records)
            4. Policy approval and delivery
            5. Regular premium payments
            
            TAX ADVANTAGES:
            - Tax-free death benefits
            - Tax-deferred cash value growth
            - Potential for tax-free policy loans
            """
        }

        # Create PDF files for each type of insurance
        for name, content in insurance_data.items():
            pdf_path = os.path.join(directory_path, f"{name}.pdf")
            canvas = reportlab.pdfgen.canvas.Canvas(pdf_path, pagesize=letter)
            
            # Format and add content to PDF
            text_object = canvas.beginText(50, 750)
            text_object.setFont("Helvetica", 10)
            
            # Clean up content and split into lines
            cleaned_content = content.strip()
            lines = cleaned_content.split('\n')
            
            for line in lines:
                text_object.textLine(line.strip())
            
            canvas.drawText(text_object)
            canvas.save()
            
            print(f"Created sample file: {pdf_path}")

    except Exception as e:
        logger.error(f"Error creating sample insurance files: {str(e)}")
        # If PDF creation fails, create text files instead
        try:
            for name, content in insurance_data.items():
                txt_path = os.path.join(directory_path, f"{name}.txt")
                with open(txt_path, 'w') as f:
                    f.write(content)
                print(f"Created sample text file: {txt_path}")
        except Exception as txt_error:
            logger.error(f"Error creating sample text files: {str(txt_error)}")


def create_fallback_document():
    """Create a fallback document in case sample files cannot be generated."""
    return """
    INSURANCE POLICIES OVERVIEW
    
    AUTO INSURANCE:
    Coverage includes liability, collision, comprehensive, personal injury protection, 
    and uninsured/underinsured motorist protection. Premiums are affected by driving history, 
    vehicle type, location, and annual mileage. Most policies have deductibles ranging from $250-$1,000.
    
    HEALTH INSURANCE:
    Common plan types include HMO, PPO, HDHP, and EPO. Coverage typically includes preventive care, 
    emergency services, hospitalization, prescription drugs, and mental health services. 
    Costs include premiums, deductibles, copayments, and coinsurance.
    
    HOME INSURANCE:
    Covers dwelling, personal property, liability, and additional living expenses. 
    Policy types range from basic HO-1 to comprehensive HO-5. Claims process involves 
    documenting damage, contacting the insurer, completing forms, meeting with an adjuster, 
    and obtaining repair estimates.
    
    LIFE INSURANCE:
    Available as term life (temporary) or permanent (whole life, universal life, variable life). 
    Eligibility depends on age, health, family history, and lifestyle choices. 
    Death benefits are generally tax-free to beneficiaries.
    """

# Additional function to convert Document objects to the format needed for the chatbot
from langchain_core.documents import Document

def document_to_dict(doc):
    """Convert a Document object to a dictionary for JSON serialization."""
    return {
        "page_content": doc.page_content,
        "metadata": doc.metadata
    }

def dict_to_document(doc_dict):
    """Convert a dictionary back to a Document object."""
    return Document(
        page_content=doc_dict["page_content"],
        metadata=doc_dict["metadata"]
    )