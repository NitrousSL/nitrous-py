def clean_phone(phone):
    return ''.join(filter(str.isdigit, phone))
