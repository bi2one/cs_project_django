def get_parent(member_type):
    if member_type == "consumer":
        return "retailer"
    elif member_type == "retailer":
        return "wholesaler"
    elif member_type == "wholesaler":
        return "factory"
    else:
        return None
