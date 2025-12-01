"""Example usage of the Florida Retirement Resources Multi-Agent System."""

from main import RetirementResourcesApp


def example_queries():
    """Run example queries to demonstrate the system."""
    
    print("=" * 70)
    print("Florida Retirement Resources - Example Queries")
    print("=" * 70)
    print()
    
    # Initialize the application
    app = RetirementResourcesApp()
    
    # Example queries
    examples = [
        "What is Medicare Part B and how much does it cost?",
        "I'm 65 and live in Miami. What Medicare plans are available?",
        "What are the income limits for Florida Medicaid?",
        "I need help finding a senior center in Orlando",
        "Can you help me understand the difference between Medicare and Medicaid?",
    ]
    
    for i, query in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"Example {i}: {query}")
        print('='*70)
        print()
        
        response = app.chat(query)
        print(f"Response:\n{response}\n")
        print("-" * 70)
        
        # Small delay for readability
        import time
        time.sleep(1)


if __name__ == "__main__":
    example_queries()

