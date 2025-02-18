import json

def save_to_json(new_entry, filename="responses.txt"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)  # load existing data
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # if file doesn't exist or is empty, start with an empty list

    # Append the new entry to the existing data
    data.append(new_entry)

    # save the updated data
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)