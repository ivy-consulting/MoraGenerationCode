def distribute_time_equally(start, end, text, decimals=4):
    """
    Distributes the time among the symbols of a word, excluding specific symbols.
    Symbols in 'filtered_text' at the start are grouped with the next symbol.
    Other symbols in 'filtered_text' are grouped with the preceding symbol.

    Parameters:
    - start (float): Start time.
    - end (float): End time.
    - text (str): The text to distribute time over.
    - decimals (int): Number of decimal places to round the time values.

    Returns:
    - list: A list of dictionaries, each containing the symbol (or symbol group) and its start and end times.
    """
    filtered_text = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']
    
    # Initialize variables
    grouped_symbols = []
    i = 0
    
    # Special case for the first symbol
    if text[0] in filtered_text and len(text) > 1:
        grouped_symbols.append(text[0] + text[1])
        i = 2  # Skip the next symbol since it's already grouped
    
    # Group symbols, excluding specific ones as per the filtered list
    while i < len(text):
        current_symbol = text[i]
        next_symbol = text[i + 1] if i + 1 < len(text) else ""
        
        # Group current symbol with next if next symbol is in filtered_text
        if next_symbol in filtered_text:
            grouped_symbols.append(current_symbol + next_symbol)
            i += 2  # Skip the next symbol
        else:
            grouped_symbols.append(current_symbol)
            i += 1
    
    duration = end - start
    num_grouped_symbols = len(grouped_symbols)
    duration_per_group = duration / num_grouped_symbols
    
    symbols_times = []
    for i, symbol_group in enumerate(grouped_symbols):
        symbol_start = start + i * duration_per_group
        symbol_end = symbol_start + duration_per_group
        symbols_times.append({
            "symbol": symbol_group,
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals),
            "vowel_consonant_length ": round(symbol_end - symbol_start, decimals)
        })
    
    return symbols_times

# Example usage
start_time = 0
end_time = 10
text = "ットはありますか?"
# Print the result to see how time is distributed
symbols_times = distribute_time_equally(start_time, end_time, text)
for symbol_time in symbols_times:
    print(symbol_time)
