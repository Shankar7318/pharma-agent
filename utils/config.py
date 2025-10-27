import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for the Pharmaceutical Agentic AI system"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', 'your_serpapi_key_optional')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Research Settings
    DEFAULT_THERAPY_AREAS = [
        "respiratory", "oncology", "cardiology", "neurology", 
        "metabolic", "infectious_diseases", "immunology", "rare_diseases"
    ]
    
    SUPPORTED_MOLECULES = [
        "metformin", "ivermectin", "remdesivir", "aspirin",
        "atorvastatin", "sildenafil", "doxycycline"
    ]
    
    # Agent Configuration
    AGENT_SETTINGS = {
        "llm_model": "gpt-4",
        "temperature": 0.1,
        "max_iterations": 3,
        "verbose": True
    }
    
    # Data Sources
    DATA_SOURCES = {
        "market_data": ["IQVIA", "EvaluatePharma", "GlobalData"],
        "clinical_trials": ["ClinicalTrials.gov", "WHO ICTRP", "EU Clinical Trials Register"],
        "patents": ["USPTO", "EPO", "WIPO"],
        "regulatory": ["FDA", "EMA", "PMDA"]
    }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        validation = {
            "openai_api_key": bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != 'your_openai_api_key_here'),
            "debug_mode": cls.DEBUG,
            "supported_therapy_areas": len(cls.DEFAULT_THERAPY_AREAS),
            "supported_molecules": len(cls.SUPPORTED_MOLECULES),
            "agent_settings": cls.AGENT_SETTINGS
        }
        
        validation["is_valid"] = all([
            validation["openai_api_key"],
            validation["supported_therapy_areas"] > 0,
            validation["supported_molecules"] > 0
        ])
        
        return validation
    
    @classmethod
    def get_agent_config(cls, agent_type: str) -> Dict[str, Any]:
        """Get configuration for specific agent type"""
        base_config = cls.AGENT_SETTINGS.copy()
        
        agent_specific = {
            "market_intelligence": {"temperature": 0.1, "max_iterations": 2},
            "patent_analysis": {"temperature": 0.1, "max_iterations": 3},
            "clinical_trials": {"temperature": 0.1, "max_iterations": 2},
            "report_generator": {"temperature": 0.3, "max_iterations": 1}
        }
        
        base_config.update(agent_specific.get(agent_type, {}))
        return base_config


class DatabaseConfig:
    """Database configuration settings"""
    
    # In a real implementation, these would come from environment variables
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'pharma_research')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Get database connection string"""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"


class APIConfig:
    """External API configuration"""
    
    # FDA API
    FDA_API_BASE = "https://api.fda.gov"
    FDA_API_KEY = os.getenv('FDA_API_KEY', '')
    
    # ClinicalTrials.gov API
    CLINICAL_TRIALS_API = "https://clinicaltrials.gov/api/v2"
    
    # USPTO API
    USPTO_API_BASE = "https://developer.uspto.gov"
    
    # Timeout settings
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Rate limiting
    REQUESTS_PER_MINUTE = 60
    
    # Cache settings
    CACHE_DURATION = 3600  # 1 hour
    
    @classmethod
    def get_api_headers(cls, api_name: str) -> Dict[str, str]:
        """Get headers for specific API"""
        headers = {
            "User-Agent": "Pharmaceutical-Agentic-AI/1.0",
            "Content-Type": "application/json"
        }
        
        if api_name == "fda" and cls.FDA_API_KEY:
            headers["Authorization"] = f"Bearer {cls.FDA_API_KEY}"
        
        return headers