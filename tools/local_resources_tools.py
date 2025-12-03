"""Local Florida resources tools for retirees."""

from typing import Dict, List, Optional


def get_local_resource(resource_type: str, city: str, zip_code: Optional[str] = None) -> str:
    """Get information about local Florida resources for retirees.
    
    Args:
        resource_type: Type of resource (e.g., "healthcare", "housing", "transportation", 
                       "senior center", "legal aid", "nutrition", "recreation")
        city: City name in Florida
        zip_code: Optional zip code for more specific results
    
    Returns:
        Information about local resources
    """
    # Mock local resources database - in production, this would query Florida state/local databases
    local_resources: Dict[str, Dict[str, List[str]]] = {
        "miami": {
            "healthcare": [
                "Jackson Memorial Hospital - Senior Services: (305) 585-1111",
                "Miami-Dade Elder Services: (305) 671-7200",
                "Community Health of South Florida: (305) 253-5100",
            ],
            "housing": [
                "Miami-Dade Housing Authority: (305) 403-6000",
                "Elderly Housing Development: (305) 375-4000",
                "Section 8 Housing Vouchers: Apply at miamidade.gov/housing",
            ],
            "transportation": [
                "Miami-Dade Transit Senior Discount: (305) 891-3131",
                "Special Transportation Services (STS): (305) 891-3131",
                "Elderly Transportation Program: Contact local senior centers",
            ],
            "senior center": [
                "Miami Beach Senior Center: (305) 673-7700",
                "Coral Gables Senior Center: (305) 460-5600",
                "North Miami Senior Center: (305) 895-9800",
            ],
        },
        "orlando": {
            "healthcare": [
                "Orlando Health Senior Services: (321) 841-5111",
                "AdventHealth Senior Care: (407) 303-5600",
                "Orange County Health Department: (407) 858-1400",
            ],
            "housing": [
                "Orlando Housing Authority: (407) 895-3300",
                "Orange County Housing Authority: (407) 895-3300",
                "Affordable Senior Housing Directory: Contact (407) 836-6500",
            ],
            "transportation": [
                "Lynx Senior Discount: (407) 841-2279",
                "Access Lynx (Paratransit): (407) 841-2279",
                "Senior Transportation Services: Contact local senior centers",
            ],
            "senior center": [
                "Orlando Senior Center: (407) 246-4483",
                "Winter Park Senior Center: (407) 599-3337",
                "Kissimmee Senior Center: (407) 870-7700",
            ],
        },
        "tampa": {
            "healthcare": [
                "Tampa General Hospital Senior Services: (813) 844-7000",
                "BayCare Senior Care: (813) 871-2000",
                "Hillsborough County Health Department: (813) 307-8000",
            ],
            "housing": [
                "Tampa Housing Authority: (813) 253-0551",
                "Hillsborough County Housing Authority: (813) 672-5400",
                "Senior Housing Resources: (813) 272-5040",
            ],
            "transportation": [
                "HART Senior Discount: (813) 254-4278",
                "HART Plus (Paratransit): (813) 254-4278",
                "Senior Transportation Network: Contact (813) 272-5040",
            ],
            "senior center": [
                "Tampa Senior Center: (813) 274-8181",
                "Hyde Park Senior Center: (813) 251-2177",
                "North Tampa Senior Center: (813) 975-2121",
            ],
        },
    }
    
    city_lower = city.lower().strip()
    resource_lower = resource_type.lower().strip()
    
    if city_lower not in local_resources:
        return (
            f"Resources for {city} not found in database. "
            "Available cities: Miami, Orlando, Tampa. "
            "For resources in other areas, contact your local Area Agency on Aging: 1-800-963-5337"
        )
    
    if resource_lower not in local_resources[city_lower]:
        return (
            f"{resource_type} resources not found for {city}. "
            "Available resource types: healthcare, housing, transportation, senior center. "
            "Contact local Area Agency on Aging for more information: 1-800-963-5337"
        )
    
    resources = local_resources[city_lower][resource_lower]
    
    result = f"{resource_type.title()} Resources in {city.title()}:\n\n"
    for i, resource in enumerate(resources, 1):
        result += f"{i}. {resource}\n"
    
    result += f"\nZip code provided: {zip_code if zip_code else 'Not specified'}\n"
    result += "\nFor additional resources, contact:\n"
    result += "- Florida Department of Elder Affairs: elderaffairs.org\n"
    result += "- Area Agency on Aging: 1-800-963-5337\n"
    result += "- Local ADRC (Aging and Disability Resource Center)"
    
    return result


def find_healthcare_facilities(city: str, facility_type: str = "all") -> str:
    """Find healthcare facilities in a Florida city.
    
    Args:
        city: City name in Florida
        facility_type: Type of facility ("hospital", "clinic", "specialist", "all")
    
    Returns:
        List of healthcare facilities
    """
    return get_local_resource("healthcare", city)


def find_housing_resources(city: str, housing_type: str = "all") -> str:
    """Find housing resources in a Florida city.
    
    Args:
        city: City name in Florida
        housing_type: Type of housing ("affordable", "senior", "assisted living", "all")
    
    Returns:
        List of housing resources
    """
    return get_local_resource("housing", city)


def find_transportation_resources(city: str) -> str:
    """Find transportation resources in a Florida city.
    
    Args:
        city: City name in Florida
    
    Returns:
        List of transportation resources
    """
    return get_local_resource("transportation", city)


def find_senior_centers(city: str) -> str:
    """Find senior centers in a Florida city.
    
    Args:
        city: City name in Florida
    
    Returns:
        List of senior centers
    """
    return get_local_resource("senior center", city)



