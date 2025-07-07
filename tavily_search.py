import os
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_person(name: str):
    """
    Searches for a person using the Tavily API and returns information about them.

    Args:
        name: The name of the person to search for.

    Returns:
        A dictionary containing the search results, or None if the API key is not set.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY environment variable not set.")
        return None

    client = TavilyClient(api_key)

    # Construct a detailed query for better results
    query = f"Who is {name}? What are their contact details, social media profiles, and recent activities?"

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            include_answer=True,
            max_results=5
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace "<person's name>" with the actual name you want to search for
    person_name = "Mr.Beast"
    results = search_person(person_name)

    if results:
        print(f"--- Search Results for {person_name} ---")
        if 'answer' in results and results['answer']:
            print("\nAI-generated Answer:")
            print(results['answer'])

        if 'results' in results and results['results']:
            print("\nSources:")
            for result in results['results']:
                print(f"- Title: {result['title']}")
                print(f"  URL: {result['url']}")
                print(f"  Content Snippet: {result['content']}\n")
