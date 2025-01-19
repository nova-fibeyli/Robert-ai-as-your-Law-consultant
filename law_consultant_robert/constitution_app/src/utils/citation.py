def cite_article(article_number, constitution):
    for article in constitution.get("articles", []):
        if article["number"] == article_number:
            return article["content"]
    return "Article not found."
