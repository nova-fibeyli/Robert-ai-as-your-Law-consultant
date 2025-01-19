def handle_question(query, constitution):
    for article in constitution.get("articles", []):
        if query.lower() in article["content"].lower():
            return article["content"]
    return "Sorry, I could not find an answer to your question."
