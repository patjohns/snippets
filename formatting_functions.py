def strip_time_from_date(input_date: str) -> str:
    try:
        # Try parsing with 12-hour format (with AM/PM)
        return dt.strptime(input_date, "%Y-%m-%d %I:%M:%S %p").strftime('%B %d, %Y').replace(' 0', ' ')
    except ValueError:
        # Fallback to parsing date without time
        return dt.strptime(input_date, "%Y-%m-%d").strftime('%B %d, %Y').replace(' 0', ' ')

def smart_title(text) -> str:
    exceptions = {'and', 'of', 'the', 'in', 'on', 'at', 'for', 'to', 'a', 'an'}
    words = text.split()
    titled = [w.capitalize() if w.lower() not in exceptions or i == 0 else w.lower()
              for i, w in enumerate(words)]
    return ' '.join(titled)

def sanitize_filename(name) -> str:
    # Replace invalid characters with spaces
    return re.sub(r'[\\/*?:"<>|]', ' ', name)
