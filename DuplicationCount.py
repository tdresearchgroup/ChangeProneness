# Jay Huskins

import os, re

def get_file_duplicates(filename, line_trim = 1, count_trim = 2, duplicates = {}):
	with open(filename) as f:
		lines = f.readlines()

	for line in lines:
		cur_line = line.strip()
		cur_line = cur_line.replace(","," ")
		#skip line if it only contains whitespace or is shorter than line_trim cutoff
		if not re.match('\w', cur_line) or len(cur_line) < line_trim:
			continue

		if cur_line in duplicates.keys():
			duplicates[cur_line] += 1
		else:
			duplicates[cur_line] = 1

	for key in duplicates.keys():
		if duplicates[key] < count_trim:
			duplicates.pop(key, None)

	return duplicates


def get_dir_duplicates(directory, line_trim = 1, count_trim = 2, write_to = None, filetype= 'java'):
	duplicates = {}
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.endswith("."+ filetype):		
				filename = os.path.join(root, file).replace("\\","/")
				with open(filename) as f:
					lines = f.readlines()

				for line in lines:
					cur_line = line.strip()
					cur_line = cur_line.replace(","," ")
					#skip line if it only contains whitespace or is shorter than line_trim cutoff
					if not re.match('\w', cur_line) or len(cur_line) < line_trim or line.startswith("import "):
						continue

					if cur_line in duplicates.keys():
						duplicates[cur_line][0] += 1
						duplicates[cur_line].append(filename)
					else:
						duplicates[cur_line] = [1]

	text = ''
	for line in duplicates.keys():
		count =  duplicates[line][0]
		if count < count_trim:
			duplicates.pop(line, None)
		else:
			text += ",".join([str(count), line] + duplicates[line][1:]) + "\n"

	if write_to:
		if not write_to.endswith(".csv"):
			write_to += ".csv"
		header = ["Duplications, Line, Sources..."]
		with open(write_to, 'w') as f:
			f.write(",".join(header) + "\n" + text)			

	return duplicates


if __name__ == "__main__":

	get_dir_duplicates("../mahout/", 30, 15, "mahout_duplicates" )

	#duplication within each file for version
	#duplication within all files for version
	#duplication between versions
