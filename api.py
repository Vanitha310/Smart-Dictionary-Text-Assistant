import requests

word_cache = {}

def fetch_word_data(word):
    word = word.lower().strip(".,!?;:\"() ")
    if not word:
        return None
    
    if word in word_cache:
        return word_cache[word]
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        meaning = data[0]["meanings"][0]
        definition = meaning["definitions"][0]["definition"]
        
        synonyms = meaning["definitions"][0].get("synonyms", [])
        example = meaning["definitions"][0].get("example", "No example available.")
        
        result = {
            "definition": definition,
            "synonyms": synonyms[:5],
            "example": example
        }
        
        word_cache[word] = result
        return result
    
    except Exception:
        return None