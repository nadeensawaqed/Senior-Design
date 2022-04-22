import yaml
address_dict = {0: 'North Classroom\nUniversity of Colorado\nDenver, CO 80204',
                1: 'Science Building\nUniversity of Colorado\nDenver, CO 80204'}

with open("address_database.yaml", "w") as f:
    yaml.dump(address_dict, f)