import json
import random
import copy
import argparse

parser = argparse.ArgumentParser("split the input into separate files")
parser.add_argument("input_file")

args = parser.parse_args()

# output_file = open("cleaned_data.json", "w")

#80%
training_file = open("training_data.json", "w")

#10%
development_file_1 = open("development_data_rating_review.json", "w")
development_file_2 = open("development_data_review.json", "w")
development_file_3 = open("development_data_rating.json", "w")

#10%
test_file_1 = open("test_data_review.json", "w")
test_file_2 = open("test_data_rating.json", "w")


input_file = open(args.input_file, "r")
input_file = input_file.read()

split_input_file = input_file.split("\n")

things_to_keep = ["reviewText", "overall"]

for i in range(len(split_input_file)):
	where_it_goes = random.randint(1,11)

	line = split_input_file[i]
	new_json = json.loads(line)
	# print(new_json)

	for element in list(new_json):
		# print(element)
		if not element in things_to_keep:
			# print("removed", element)
			new_json.pop(element, None)

	# print(new_json)

	new_json["id"] = i

	if where_it_goes >= 1 and where_it_goes <= 8:
		json.dump(new_json, training_file)
		training_file.write("\n")
	elif where_it_goes == 9:
		json.dump(new_json, development_file_1)
		development_file_1.write("\n")

		new_json_2 = copy.deepcopy(new_json)
		new_json_2.pop("overall", None)
		json.dump(new_json_2, development_file_2)
		development_file_2.write("\n")

		new_json_3 = copy.deepcopy(new_json)
		new_json_3.pop("reviewText", None)
		json.dump(new_json_3, development_file_3)
		development_file_3.write("\n")
	else:
		new_json_2 = copy.deepcopy(new_json)
		new_json_2.pop("overall", None)
		json.dump(new_json_2, test_file_1)
		test_file_1.write("\n")

		new_json_3 = copy.deepcopy(new_json)
		new_json_3.pop("reviewText", None)
		json.dump(new_json_3, test_file_2)
		test_file_2.write("\n")



	# json.dump(new_json, output_file)
	# output_file.write("\n")
