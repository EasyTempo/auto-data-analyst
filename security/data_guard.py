import pandas as pd
import re

class DataPrivacyGuard:
    """
    DataPrivacyGuard is responsible for inspecting data and redacting PII
    (Personally Identifiable Information) before it is processed by the LLM.
    This fulfills the Security requirement for the Capstone project.
    """
    
    # Simple regex patterns for demonstration
    PII_PATTERNS = {
        'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b'
    }

    @staticmethod
    def redact_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Scans object/string columns and redacts detected PII.
        Returns a new redacted DataFrame.
        """
        redacted_df = df.copy()
        for col in redacted_df.select_dtypes(include=['object', 'string']).columns:
            # We iterate over patterns and replace occurrences
            for pii_type, pattern in DataPrivacyGuard.PII_PATTERNS.items():
                redacted_df[col] = redacted_df[col].apply(
                    lambda x: re.sub(pattern, f'[REDACTED {pii_type.upper()}]', str(x)) if pd.notnull(x) else x
                )
        return redacted_df

    @staticmethod
    def extract_safe_metadata(df: pd.DataFrame) -> str:
        """
        Extracts column names, data types, and safe summary statistics 
        to send to the LLM without leaking raw data.
        """
        # We only send column names, dtypes, and basic stats
        metadata = f"Data Shape: {df.shape}\n\n"
        metadata += "Columns and Data Types:\n"
        metadata += str(df.dtypes) + "\n\n"
        
        # Add basic numeric description, skipping string data which might contain PII
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            metadata += "Numeric Data Summary:\n"
            metadata += str(numeric_df.describe())
            
        return metadata

if __name__ == "__main__":
    # Quick test
    df_test = pd.DataFrame({
        "id": [1, 2],
        "name": ["Alice", "Bob"],
        "contact": ["alice@email.com", "Call 555-123-4567"]
    })
    print("Original:\n", df_test)
    print("\nRedacted:\n", DataPrivacyGuard.redact_dataframe(df_test))
