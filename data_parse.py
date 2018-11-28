import json

output_file = open("cleaned_data.json", "w")

input_file = open("small_small_data.json", "r")
input_file = input_file.read()

split_input_file = input_file.split("\n")

# print(split_input_file)
# print(len(split_input_file))

things_to_keep = ["reviewText", "overall"]

for i in range(len(split_input_file)):
# for line in split_input_file:
	line = split_input_file[i]
	new_json = json.loads(line)
	print(new_json)

	for element in list(new_json):
		print(element)
		if not element in things_to_keep:
			print("removed", element)
			new_json.pop(element, None)

	new_json["id"] = i
	print(new_json)

	json.dump(new_json, output_file)
	output_file.write("\n")

