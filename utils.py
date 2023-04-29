
def assign_operator_properties(operator, **kwargs):
    for key, value in kwargs.items():
        setattr(operator, key, value)