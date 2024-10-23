import wikipedia

def get_factual_answer(query):
    try:
        query - query.replace("who is", "").replace("what is", "").strip()
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Can you be more specific? Did you mean {e.options[:5]}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything related to that."