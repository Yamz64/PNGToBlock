#include "TileGenerator.h"

#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <format>

//struct to help in the storing of command data
struct CommandData {
public:
	std::string name;
	std::vector<std::string> args;
};

//function to help with returning lowercase strings
std::string lower(const char* &str) {
	std::string o_str = "";
	for (unsigned int i = 0; i < strlen(str); i++) {
		if (str[i] >= 'A' && str[i] <= 'Z')
			o_str += str[i] + 32;
		else
			o_str += str[i];
	}
	return o_str;
}

//if input provided from the console is invalid then do some error checking, output the error, and return false, otherwise return true
bool ValidateInput(int argc, const char** argv, std::vector<CommandData>& outputted_commands) {
	//invalid number of arguments for the default commandline argument
	if (argc != 3 && argc < 4) {
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
	//special argument check
	if (argc > 3) {
		bool found_special = false;
		for (unsigned int i = 3; i < argc; i++) {
			//-s <output filename> <plane> <flipU?> <flipV?> <palette>
			std::string special_character = argv[i];
			if (special_character == "-s") {
				found_special = true;
				//check if there are enough arguments in the commandline
				if (i + 5 > argc - 1) {
					std::cerr << "[ERROR]: -s takes 6 arguments: <input image> <output filename> <plane> <flipU?> <flipV?> <palette>" << std::endl;
					return false;
				}

				//check if the output filename has a .schem extension
				std::string output_schem_string = argv[i + 1];
				if (output_schem_string.size() < 6) {
					std::cerr << "[ERROR]: output schematic must be of filetype '.schem'!" << std::endl;
					return false;
				}

				if (output_schem_string.substr(output_schem_string.size() - 6, output_schem_string.size() - 1) != ".schem") {
					std::cerr << "[ERROR]: output schematic must be of filetype '.schem'!" << std::endl;
					return false;
				}

				//check if the plane is valid
				if (lower(argv[i + 2]) != "xy" && lower(argv[i + 2]) != "yz") {
					std::cerr << "[ERROR]: outputted plane should be either: 'XY', or 'YZ'!" << std::endl;
					return false;
				}

				//check if flipu is valid
				if (lower(argv[i + 3]) != "true" && lower(argv[i + 3]) != "false" && argv[i + 3] != "0" && argv[i + 3] != "1") {
					std::cerr << "[ERROR]: flipU must either be true or false!" << std::endl;
					return false;
				}

				//check if flipv is valid
				if (lower(argv[i + 4]) != "true" && lower(argv[i + 4]) != "false" && argv[i + 4] != "0" && argv[i + 4] != "1") {
					std::cerr << "[ERROR]: flipV must either be true or false!" << std::endl;
					return false;
				}

				//add this command to the command list since everything passed
				CommandData s_command;
				s_command.name = "-s";
				s_command.args.push_back(argv[2]);
				s_command.args.push_back(argv[i + 1]);
				s_command.args.push_back(argv[i + 2]);
				s_command.args.push_back(argv[i + 3]);
				s_command.args.push_back(argv[i + 4]);
				s_command.args.push_back(argv[i + 5]);
				outputted_commands.push_back(s_command);
			}
		}

		//did not find a special argument
		if (!found_special) {
			std::cerr << "[ERROR]: no special arguments provided, matched any known special arguments!" << std::endl;
			return false;
		}
	}

	//everything worked properly
	ifile.close();
	return true;
}

//function will execute all special arguments provided to the program
void ExecuteSpecialArgs(std::vector<CommandData> out_commands) {
	for (unsigned int i = 0; i < out_commands.size(); i++) {
		//-s
		if (out_commands[i].name == "-s") {
			std::string outputted_command = "";
			outputted_command = std::format("py PNGToSchem/main.py {} {} {} {} {} {}", out_commands[i].args[0], out_commands[i].args[1]
				, out_commands[i].args[2], out_commands[i].args[3], out_commands[i].args[4], out_commands[i].args[5]);

			system(outputted_command.c_str());
		}
	}

}

int main(int argc, const char** argv) {
	std::vector<CommandData> outputted_commands;
	bool execute = ValidateInput(argc, argv, outputted_commands);
	if (!execute)
		return 1;
	{
		TileGenerator generator = TileGenerator(argv[1], argv[2]);
		ExecuteSpecialArgs(outputted_commands);
	}
	return 0;
}