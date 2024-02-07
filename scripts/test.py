def remove_symbols_from_text(text, symbols):
    """
    Remove all instances of specified symbols from the text using list comprehension.

    Parameters:
    - text (str): The original text from which symbols will be removed.
    - symbols (list): A list of symbols (strings) to be removed from the text.

    Returns:
    - str: The text with the specified symbols removed.
    """
    return ''.join([char for char in text if char not in symbols])

# Ejemplo de uso
text = "¡Hola, mundo! ¿Todo bien?"
symbols = ["¡", "!", "?", ","]

cleaned_text = remove_symbols_from_text(text, symbols)
print(cleaned_text)  # Salida: "Hola mundo Todo bien"
