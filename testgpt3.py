import openai

openai.api_key = "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"

def generate_book_name(keyword):
    prompt = (f"Generate a book name based on the keyword '{keyword}'. Name:")

    # Generate book name, if book name is too short or too long, try again
    book_name = "a"*51
    while len(book_name) < 5 or len(book_name) > 50:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        book_name = response.choices[0].text.strip()

    return book_name


book_name = generate_book_name("melody lady")
print(book_name)