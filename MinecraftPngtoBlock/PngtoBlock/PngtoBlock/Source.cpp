#include "TileGenerator.h"

#include <iostream>
#include <fstream>
#include <string>

//if input provided from the console is invalid then do some error checking, output the error, and return false, otherwise return true
bool ValidateInput(int argc, const char** argv) {
	//invalid number of arguments
	if (argc != 3) {
		std::cerr << "[ERROR]: Invalid number of arguments provided: " << argc - 1 << " given, when 2 are needed!" << std::endl;
		std::cout << "Proper usage: \"./PngtoBlock <input file directory> <output file directory>\"" << std::endl;
		return false;
	}

	//input file isn't a valid path
	std::ifstream ifile(argv[1]);
	if (!ifile) {
		std::cerr << "[ERROR]: Invalid filepath for input file given! " << argv[1] << " does not exist!" << std::endl;
		return false;
	}

	//input file isn't a .png
	const char* extension = ".png";
	std::string ifilestring = argv[1];

	int j = 0;
	for (unsigned int i = ifilestring.size() - 4; i < ifilestring.size(); i++) {
		if (ifilestring[i] != extension[j]) {
			std::cerr << "[ERROR]: Input file must be a .png!" << std::endl;
			return false;
		}
		j++;
	}

	//everything worked properly
	ifile.close();
	return true;
}

int main(int argc, const char** argv) {
	bool execute = ValidateInput(argc, argv);
	if (!execute)
		return 1;
	{
		TileGenerator generator = TileGenerator(argv[1], argv[2]);
	}
	return 0;
}