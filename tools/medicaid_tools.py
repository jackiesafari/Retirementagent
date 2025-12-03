"""Medicaid-related tools for the retirement resources system."""

from typing import Dict, Tuple


def get_medicaid_info(topic: str) -> str:
    """Get information about Florida Medicaid topics.
    
    Args:
        topic: Medicaid topic to look up (e.g., "eligibility", "application", 
               "long term care", "nursing home", "home care", "income limits", 
               "asset limits", "waiver programs")
    
    Returns:
        Detailed information about the Medicaid topic as a string
    """
    # Mock Medicaid knowledge base - in production, this would query Florida Medicaid databases
    medicaid_knowledge_base: Dict[str, str] = {
        "eligibility": (
            "Florida Medicaid Eligibility:\n"
            "- Income limits vary by program and household size\n"
            "- Aged/Disabled: Income limit ~$1,215/month for individuals (2024)\n"
            "- Asset limits: $2,000 for individuals, $3,000 for couples (some programs)\n"
            "- Must be U.S. citizen or qualified immigrant\n"
            "- Must be Florida resident\n"
            "- Must meet categorical requirements (aged 65+, disabled, or blind)\n"
            "- Different rules apply for Long-Term Care Medicaid"
        ),
        "application": (
            "How to Apply for Florida Medicaid:\n"
            "- Apply online: myflorida.com/accessflorida\n"
            "- Apply by phone: 1-866-762-2237\n"
            "- Apply in person: Local Department of Children and Families office\n"
            "- Required documents: ID, proof of income, proof of assets, proof of residency\n"
            "- Application processing: 30-45 days typically\n"
            "- Can apply for multiple programs simultaneously"
        ),
        "long term care": (
            "Florida Medicaid Long-Term Care:\n"
            "- Covers nursing home care for eligible individuals\n"
            "- Income limit: $2,829/month (2024) for nursing home care\n"
            "- Asset limit: $2,000 (individual), $3,000 (couple)\n"
            "- Look-back period: 5 years for asset transfers\n"
            "- Spousal impoverishment protections available\n"
            "- Requires functional need assessment"
        ),
        "nursing home": (
            "Medicaid Nursing Home Coverage:\n"
            "- Covers room, board, and medical care in Medicaid-certified facilities\n"
            "- Must meet income and asset requirements\n"
            "- Must require nursing home level of care\n"
            "- Personal needs allowance: $130/month (2024)\n"
            "- Spouse can keep income and assets under spousal impoverishment rules\n"
            "- Estate recovery may apply after death"
        ),
        "home care": (
            "Medicaid Home and Community-Based Services:\n"
            "- Waiver programs allow care at home instead of nursing home\n"
            "- Programs: Aged and Disabled Adult (ADA) Waiver, Statewide Medicaid Managed Care\n"
            "- Services may include: personal care, homemaker services, adult day care\n"
            "- Must meet functional and financial eligibility\n"
            "- Wait lists may exist for some waiver programs\n"
            "- Contact local Aging and Disability Resource Center (ADRC)"
        ),
        "income limits": (
            "Florida Medicaid Income Limits (2024):\n"
            "- Aged/Disabled (SSI-related): $1,215/month (individual)\n"
            "- Long-Term Care: $2,829/month (nursing home)\n"
            "- Home and Community-Based Services: Varies by program\n"
            "- Income includes: Social Security, pensions, interest, dividends\n"
            "- Some income may be excluded (e.g., Medicare premiums)\n"
            "- Income limits increase annually"
        ),
        "asset limits": (
            "Florida Medicaid Asset Limits (2024):\n"
            "- Standard: $2,000 (individual), $3,000 (couple)\n"
            "- Exempt assets: Home (if living there or spouse), one vehicle, personal belongings\n"
            "- Exempt assets: Prepaid funeral, certain life insurance\n"
            "- Countable assets: Bank accounts, investments, second homes, additional vehicles\n"
            "- 5-year look-back period for asset transfers\n"
            "- Different rules for Long-Term Care vs. regular Medicaid"
        ),
        "waiver programs": (
            "Florida Medicaid Waiver Programs:\n"
            "- Aged and Disabled Adult (ADA) Waiver: Home and community-based services\n"
            "- Statewide Medicaid Managed Care Long-Term Care: Comprehensive managed care\n"
            "- Program of All-Inclusive Care for the Elderly (PACE): Day center-based care\n"
            "- Services vary by program and may include: personal care, respite, adult day care\n"
            "- Must meet functional and financial eligibility\n"
            "- Contact ADRC for assessment and enrollment"
        ),
        "florida specific": (
            "Florida Medicaid Resources:\n"
            "- Apply: myflorida.com/accessflorida or 1-866-762-2237\n"
            "- State Medicaid Agency: Agency for Health Care Administration (AHCA)\n"
            "- Aging and Disability Resource Centers (ADRC): Local offices throughout Florida\n"
            "- SHIP (State Health Insurance Assistance Program): 1-800-963-5337\n"
            "- Florida Department of Elder Affairs: elderaffairs.org\n"
            "- Over 4.5 million Floridians enrolled in Medicaid"
        ),
    }
    
    topic_lower = topic.lower().strip()
    
    # Try exact match first
    if topic_lower in medicaid_knowledge_base:
        return medicaid_knowledge_base[topic_lower]
    
    # Try partial matches
    for key, value in medicaid_knowledge_base.items():
        if key in topic_lower or topic_lower in key:
            return value
    
    return (
        f"Information about '{topic}' not found in Medicaid knowledge base. "
        "Available topics include: eligibility, application, long term care, "
        "nursing home, home care, income limits, asset limits, waiver programs, "
        "and Florida-specific information. "
        "For detailed information, visit myflorida.com/accessflorida or call 1-866-762-2237."
    )


def check_medicaid_eligibility(monthly_income: float, assets: float, age: int, needs_long_term_care: bool = False) -> str:
    """Check preliminary Medicaid eligibility based on income and assets.
    
    Args:
        monthly_income: Monthly income in dollars
        assets: Total countable assets in dollars
        age: Age of applicant
        needs_long_term_care: Whether applicant needs long-term care services
    
    Returns:
        Preliminary eligibility assessment (note: this is not a final determination)
    """
    if age < 65:
        return (
            "Age requirement: Must be 65 or older for aged Medicaid programs. "
            "Other Medicaid categories may be available. Contact ADRC for assessment."
        )
    
    # Standard aged/disabled limits (2024)
    income_limit_standard = 1215
    asset_limit_standard = 2000
    
    # Long-term care limits (2024)
    income_limit_ltc = 2829
    asset_limit_ltc = 2000
    
    if needs_long_term_care:
        income_limit = income_limit_ltc
        asset_limit = asset_limit_ltc
        program_type = "Long-Term Care"
    else:
        income_limit = income_limit_standard
        asset_limit = asset_limit_standard
        program_type = "Standard Aged/Disabled"
    
    income_eligible = monthly_income <= income_limit
    asset_eligible = assets <= asset_limit
    
    result = f"Preliminary {program_type} Medicaid Eligibility Assessment:\n\n"
    result += f"Income: ${monthly_income:,.2f}/month (Limit: ${income_limit:,}/month)\n"
    result += f"Assets: ${assets:,.2f} (Limit: ${asset_limit:,})\n\n"
    
    if income_eligible and asset_eligible:
        result += "✅ Preliminary assessment: May be eligible\n"
        result += "Note: This is NOT a final determination. Functional needs and other factors are also considered.\n"
        result += "Next steps: Apply at myflorida.com/accessflorida or call 1-866-762-2237"
    elif not income_eligible and not asset_eligible:
        result += "❌ Preliminary assessment: May not meet income AND asset requirements\n"
        result += "Consider: Spousal impoverishment protections, asset planning (consult elder law attorney), or other programs"
    elif not income_eligible:
        result += "⚠️ Income may exceed limit\n"
        result += "Consider: Qualified Income Trust (QIT) for long-term care, or other programs"
    else:
        result += "⚠️ Assets may exceed limit\n"
        result += "Consider: Asset planning strategies (consult elder law attorney), or spend-down options"
    
    result += "\n\n⚠️ IMPORTANT: This is a preliminary assessment only. Final eligibility is determined by the state."
    
    return result



