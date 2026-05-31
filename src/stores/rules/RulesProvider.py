from typing import List


COMPLIANCE_RULES: List[str] = [
    "Documents must include a clearly defined data retention policy.",
    "Personal data must not be shared with third parties without explicit written consent.",
    "Sensitive personal data (health, biometric, financial) must be encrypted at rest and in transit.",
    "Users must be informed of data collection purposes before data is collected.",
    "All financial transactions above $10,000 must be reported to the relevant authority.",
    "Financial statements must be prepared in accordance with IFRS or GAAP standards.",
    "Any conflict of interest held by board members must be disclosed in writing.",
    "Audit trails must be maintained for all financial transactions for a minimum of 7 years.",
    "All contracts must include a liability limitation clause.",
    "Contracts involving personal data processing must include a Data Processing Agreement (DPA).",
    "Termination clauses must specify notice periods of no less than 30 days.",
    "Contracts must identify the governing law and jurisdiction.",
    "Risk assessments must be conducted before entering any new market or product line.",
    "Anti-money laundering (AML) checks must be performed on all new counterparties.",
    "Whistleblower protection policies must be documented and accessible to all employees.",
    "Business continuity plans must be reviewed and updated at least annually.",
]


def get_rules() -> List[str]:
    return COMPLIANCE_RULES
