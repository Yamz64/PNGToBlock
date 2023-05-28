import sys, os
from image_loader import ImageLoader


#function handles commandline errors, returns a boolean (true) if everything goes right
def ErrorChecking():
	#make sure that there is only a filepath provided to an image
	if(len(sys.argv) != 7):
		print(f"[ERROR]: Improper number of arguments given, {len(sys.argv) - 1} provided when 6 are expected!");
		print("Proper usage: <input image> <output filename> <plane> <flipU?> <flipV?> <palette>");
		return False;

	#make sure the filepath exists
	if(not os.path.exists(sys.argv[1])):
		print(f"[ERROR]: filepath: {sys.argv[1]} does not exist!");
		return False;

	#make sure the image provided is an image
	extensions = [".png", ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi"];
	found_extension = False;

	for extension in extensions:
		l = len(sys.argv[1]) - len(extension);
		if(sys.argv[1][l:] == extension):
			found_extension = True;
			break;

	if(not found_extension):
		print("[ERROR]: filepath provided is not a recognized image format!");
		return False;

	#make sure an output filename has been provided
	if(sys.argv[2][len(sys.argv[2]) - 6:] != ".schem"):
		print("[ERROR]: output file must be a schematic file!");
		return False;

	#make sure the plane to output at is a valid cardinal plane
	planes = ["XY", "YZ"];
	found_plane = False;

	for plane in planes:
		if(sys.argv[3].lower() == plane.lower()):
			found_plane = True;
			break;

	if(not found_plane):
		print("[ERROR]: exported plane must be 'XY' or 'YZ'!");
		return False;

	#make sure that flip U is validly inputted
	if(sys.argv[4] != "False".lower() and sys.argv[4] != "True".lower() and sys.argv[4] != "0" and sys.argv[4] != "1"):
		print("[ERROR]: flipU must be either true or false!");
		return False;

	#make sure that flip V is validly inputted
	if(sys.argv[5] != "False".lower() and sys.argv[5] != "True".lower() and sys.argv[5] != "0" and sys.argv[5] != "1"):
		print("[ERROR]: flipU must be either true or false!");
		return False;

	return True;


if __name__ == "__main__":
	if(ErrorChecking()):
		flip_u = (sys.argv[4] == "True".lower() or sys.argv[4] == "1");
		flip_v = (sys.argv[5] == "True".lower() or sys.argv[5] == "1");
		loader = ImageLoader(sys.argv[1], sys.argv[2], sys.argv[3].lower(), flip_u, flip_v, sys.argv[6]);