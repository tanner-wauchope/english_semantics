

def have(subject, complement):
    attribute_name = str(complement).lower().replace(' ', '_')
    setattr(subject, attribute_name, complement)