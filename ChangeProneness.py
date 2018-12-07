#Difference Tracker
from glob import glob
import os, difflib

def calc_diff(filename1, filename2):
	with open(filename1) as f:
		file1 = f.read()
	with open(filename2) as f:
		file2 = f.read()
	match = difflib.SequenceMatcher(lambda x: x in " \t", file1, file2)
	return match.quick_ratio()

	#ignore comments, whitespace

def folder_compare(foler1, folder2, filetype):
	#compares files in two folders
	#calc diff in *filetype* files that are in both
	#ouput which files are in one but not the other
	
	if not os.path.isdir(folder1):
		print folder1 + " doesn't exist"
		return
	if not os.path.isdir(folder2):
		print folder2 + " doesn't exist"
		return
	aFiles = glob(folder1 + "/*." + filetype)
	bFiles = glob(folder2 + "/*." + filetype)
	ratios = {}
	change = bFiles
	for afile in aFiles:
		cleanFile = afile.split("\\")[-1]
		skipped = True
		for bfile in bFiles:
			if cleanFile in bfile:
				change.remove(bfile)
				ratios[cleanFile] = (calc_diff(folder1 +"/"+ cleanFile, folder2 +"/"+ cleanFile))
				skipped = False
				break
		if skipped:
			change.append(afile)

	ratios["AVG"] = sum(ratios.values()) / len(ratios.values())

	return ratios, change

def version_compare(old_dir, new_dir, write_to = None, filetype = "java"):
	old_dir = old_dir.replace('\\',"/")
	new_dir = new_dir.replace('\\',"/")
	output = []
	diff_average = []
	old_files = {}
	old_files = {}
	additions = 0
	subtractions = 0
	for idir in [old_dir, new_dir]:
		idir = idir.replace("\\", "/")
		if not idir.endswith("/"):
			idir += "/"

		old_bool = bool(old_files)
		for root, dirs, files in os.walk( idir ):
			full_path = os.path.abspath(root).replace("\\", "/")
			short_path = full_path.split("/")[-2:]
			
			for file in files:
				if file.endswith(filetype):
					folder_file = ("/").join(short_path + [file])
					if old_bool:
						new_file = full_path +'/'+ file
						if folder_file in old_files.keys():
							old_file = old_files.pop(folder_file) +"/"+ file
							diff = 100*round(1.0 - calc_diff(new_file, old_file), 5)
							diff_average.append(diff)
							output.append([old_file, new_file, "m", str(diff)+'%'])
						else:
							output.append([" ", new_file, "+", ""])
							additions += 1
					else:
						old_files[folder_file] = full_path
	for i in old_files.keys():
		file = old_files[i] +"/"+ i.split("/")[-1]
		output.append( [file, " ", "-", ""] )
		subtractions += 1

	diff_average = sum(diff_average)/len(diff_average)
	
	header = 	[[old_dir, new_dir, "AVG Mod", str(diff_average)+'%'], 
				["SUB", str(subtractions), "ADD", str(additions)]]
	output = header + output

	if write_to:
		if not write_to.endswith(".csv"):
			write_to += ".csv"
		with open(write_to, "w") as f:
			for line in output:
				f.write( ",".join(line) + '\n' )

	return output

def system_compare(directory, write_to, filetype = "java"):
	directory = directory.replace("\\", "/")
	if not directory.endswith("/"):
		directory += "/"
	left_output = []
	folders = glob(directory + "*/")
	folders.sort(key= lambda name: int(''.join([i for i in name if i.isdigit()])))
	print folders

	for i in range(len(folders)-1):
		print(i)
		if len(left_output) == 0:
			left_output = ( version_compare(folders[i], folders[i+1]) )
		else:
			right_output = ( version_compare(folders[i], folders[i+1]) )
			left_len = len(left_output)
			right_len = len(right_output)
			blank = ['','','','','']
			for j in range(max(left_len, right_len)):
				if j >= right_len:
					left_output[j] += blank
				elif j >= left_len:
					left_output.append(blank + right_output[j])
				else:
					left_output[j] += [''] + right_output[j]

	if not write_to.endswith(".csv"):
		write_to += ".csv"
	with open(write_to, "w") as f:
		for line in left_output:
			f.write( ",".join(line) + '\n' )



if __name__ == '__main__':
	#print calc_diff("../StrategyPanel_1.java", "../StrategyPanel_5.java")
	#folder1 = "../azureus/Azureus_2.2.0.2_source/org/gudy/azureus2/platform"
	#folder2 = "../azureus/Azureus_2.3.0.2_source/org/gudy/azureus2/platform"
	# ratios, change = folder_compare(folder1, folder2, "java")

	#version_compare("../azureus/Azureus_2.2.0.2_source", "../azureus/Azureus_2.3.0.2_source", "AZ_compare")
	#system_compare("../azureus", "Azureus_sys_compare")
	system_compare("../hive", "Hive_sys_compare")
		
