"""Medicare-related tools for the retirement resources system."""

from typing import Dict, List


def get_medicare_info(topic: str) -> str:
    """Get information about Medicare topics.
    
    Args:
        topic: Medicare topic to look up (e.g., "Part A", "Part B", "Part D", 
               "enrollment", "costs", "coverage", "supplemental insurance")
    
    Returns:
        Detailed information about the Medicare topic as a string
    """
    # Mock Medicare knowledge base - in production, this would query official CMS databases
    medicare_knowledge_base: Dict[str, str] = {
        "part a": (
            "Medicare Part A (Hospital Insurance):\n"
            "- Covers inpatient hospital stays, skilled nursing facility care, hospice care, and some home health care\n"
            "- Most people don't pay a premium for Part A if they or their spouse paid Medicare taxes while working\n"
            "- 2024 deductible: $1,632 per benefit period\n"
            "- Coinsurance varies by length of stay\n"
            "- Enrollment: Automatic if receiving Social Security benefits at age 65"
        ),
        "part b": (
            "Medicare Part B (Medical Insurance):\n"
            "- Covers doctor visits, outpatient care, medical supplies, and preventive services\n"
            "- 2024 standard premium: $174.70/month (may be higher based on income)\n"
            "- Annual deductible: $240\n"
            "- Typically covers 80% of approved costs after deductible\n"
            "- Enrollment: Automatic with Part A, but can opt out\n"
            "- Late enrollment penalty: 10% per year if you don't sign up when first eligible"
        ),
        "part c": (
            "Medicare Part C (Medicare Advantage):\n"
            "- Private insurance alternative to Original Medicare (Parts A & B)\n"
            "- Often includes Part D (prescription drug coverage)\n"
            "- May include additional benefits like dental, vision, hearing\n"
            "- Must have Parts A and B to enroll\n"
            "- Costs vary by plan and location\n"
            "- Enrollment periods: Initial, Annual (Oct 15 - Dec 7), Open (Jan 1 - Mar 31)"
        ),
        "part d": (
            "Medicare Part D (Prescription Drug Coverage):\n"
            "- Helps cover the cost of prescription drugs\n"
            "- Offered by private insurance companies\n"
            "- Average premium: ~$55/month (varies by plan)\n"
            "- Late enrollment penalty: 1% per month if you don't have creditable coverage\n"
            "- Formulary (covered drugs) varies by plan\n"
            "- Coverage gap (donut hole) exists but is closing"
        ),
        "enrollment": (
            "Medicare Enrollment Information:\n"
            "- Initial Enrollment Period: 3 months before, month of, and 3 months after 65th birthday\n"
            "- General Enrollment Period: January 1 - March 31 (coverage starts July 1)\n"
            "- Special Enrollment Periods: Available for certain life events\n"
            "- Medicare Advantage Open Enrollment: January 1 - March 31\n"
            "- Annual Enrollment Period: October 15 - December 7 (for Part C and D changes)\n"
            "- Apply online at ssa.gov/medicare or call 1-800-MEDICARE"
        ),
        "costs": (
            "Medicare Costs Overview (2024):\n"
            "- Part A Premium: $0 for most people (if worked 10+ years)\n"
            "- Part A Deductible: $1,632 per benefit period\n"
            "- Part B Premium: $174.70/month (standard)\n"
            "- Part B Deductible: $240/year\n"
            "- Part D Premium: ~$55/month average (varies)\n"
            "- Medicare Advantage: Varies by plan ($0-$200+/month)\n"
            "- Medigap (Supplemental): $50-$300+/month depending on plan\n"
            "- Income-Related Monthly Adjustment Amount (IRMAA) may apply for higher incomes"
        ),
        "supplemental insurance": (
            "Medicare Supplemental Insurance (Medigap):\n"
            "- Helps pay for costs not covered by Original Medicare\n"
            "- 10 standardized plans (A, B, C, D, F, G, K, L, M, N)\n"
            "- Best time to buy: During 6-month Medigap Open Enrollment Period\n"
            "- Costs vary by plan, age, location, and insurance company\n"
            "- Cannot be used with Medicare Advantage\n"
            "- Guaranteed issue rights in certain situations"
        ),
        "florida specific": (
            "Florida Medicare Information:\n"
            "- Over 4.5 million Medicare beneficiaries in Florida\n"
            "- Many Medicare Advantage plans available\n"
            "- Popular plans: Humana, UnitedHealthcare, Blue Cross Blue Shield\n"
            "- State Health Insurance Assistance Program (SHIP): 1-800-963-5337\n"
            "- Florida Department of Elder Affairs: elderaffairs.org\n"
            "- Medicare Savings Programs available for low-income beneficiaries"
        ),
    }
    
    topic_lower = topic.lower().strip()
    
    # Try exact match first
    if topic_lower in medicare_knowledge_base:
        return medicare_knowledge_base[topic_lower]
    
    # Try partial matches
    for key, value in medicare_knowledge_base.items():
        if key in topic_lower or topic_lower in key:
            return value
    
    return (
        f"Information about '{topic}' not found in Medicare knowledge base. "
        "Available topics include: Part A, Part B, Part C, Part D, enrollment, "
        "costs, supplemental insurance, and Florida-specific information. "
        "For detailed information, visit medicare.gov or call 1-800-MEDICARE."
    )


def search_medicare_plans(zip_code: str, plan_type: str = "all") -> str:
    """Search for available Medicare plans in a specific Florida zip code.
    
    Args:
        zip_code: Florida zip code (e.g., "33101", "32801")
        plan_type: Type of plan to search for ("advantage", "supplement", "partd", "all")
    
    Returns:
        Information about available Medicare plans in the area
    """
    # Mock plan database - in production, this would query CMS plan finder API
    florida_plans: Dict[str, List[Dict[str, str]]] = {
        "33101": [  # Miami
            {"name": "Humana Gold Plus HMO", "type": "advantage", "premium": "$0", "rating": "4.5 stars"},
            {"name": "UnitedHealthcare Medicare Advantage", "type": "advantage", "premium": "$15", "rating": "4.0 stars"},
            {"name": "AARP Medicare Supplement Plan G", "type": "supplement", "premium": "$150", "rating": "4.2 stars"},
        ],
        "32801": [  # Orlando
            {"name": "Blue Cross Blue Shield Medicare Advantage", "type": "advantage", "premium": "$0", "rating": "4.3 stars"},
            {"name": "Humana Medicare Advantage", "type": "advantage", "premium": "$25", "rating": "4.1 stars"},
        ],
        "33601": [  # Tampa
            {"name": "WellCare Medicare Advantage", "type": "advantage", "premium": "$0", "rating": "4.0 stars"},
            {"name": "Aetna Medicare Advantage", "type": "advantage", "premium": "$20", "rating": "4.4 stars"},
        ],
    }
    
    zip_code_clean = zip_code.strip()
    
    if zip_code_clean not in florida_plans:
        return (
            f"Plans for zip code {zip_code} not found in database. "
            "To find plans in your area, visit medicare.gov/plan-compare or call 1-800-MEDICARE. "
            "Available sample zip codes: 33101 (Miami), 32801 (Orlando), 33601 (Tampa)."
        )
    
    plans = florida_plans[zip_code_clean]
    
    if plan_type.lower() != "all":
        plans = [p for p in plans if plan_type.lower() in p["type"].lower()]
    
    if not plans:
        return f"No {plan_type} plans found for zip code {zip_code}."
    
    result = f"Available Medicare Plans in {zip_code}:\n\n"
    for plan in plans:
        result += f"- {plan['name']} ({plan['type'].title()})\n"
        result += f"  Premium: {plan['premium']}/month\n"
        result += f"  Rating: {plan['rating']}\n\n"
    
    result += "Note: This is sample data. For real-time plan information, visit medicare.gov/plan-compare"
    
    return result

