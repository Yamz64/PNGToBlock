from PIL import Image
from nbt import nbt
from nbt.nbt import *

def GetKeyBlockDataHeight(block_data):
	return block_data[1][1];

def GetKeyBlockDataLength(block_data):
	return block_data[1][2];

def GetKeyBlockDataWidth(block_data):
	return block_data[1][0];

class ImageLoader:
	#constructor - creates this object and automatically processes/outputs the schem data
	def __init__(self, input_filepath: str, output_filename: str, plane: str, flip_u: bool, flip_v: bool, palette: str):
		self.image_data = Image.open(input_filepath);
		self.plane = plane;
		self.flip_u = flip_u;
		self.flip_v = flip_v;
		self.palette = palette;

		#actual block processing
		self.block_palette = [];
		self.block_data = [];
		self.ProcessImage();

		#initialize schem values
		self.schem = nbt.NBTFile();
		self.schem.name = output_filename;
		self.InitializeMiscSchemValues();
		self.schem.write_file(output_filename);
		print(f"Outputted file: {output_filename}!");



	def InitializeMiscSchemValues(self):
		#version
		self.schem.tags.append(TAG_Int(name="DataVersion", value = 3218));
		self.schem.tags.append(TAG_Int(name="Version", value = 2));

		#dimensions (initialized to 0, 0, 0)
		if(self.plane == "xy"):
			self.schem.tags.append(TAG_Short(name="Width", value = self.image_data.width));
			self.schem.tags.append(TAG_Short(name="Height", value = self.image_data.height));
			self.schem.tags.append(TAG_Short(name="Length", value = 1));
		else:
			self.schem.tags.append(TAG_Short(name="Width", value = 1));
			self.schem.tags.append(TAG_Short(name="Height", value = self.image_data.height));
			self.schem.tags.append(TAG_Short(name="Length", value = self.image_data.width));

		#offset (zero this out)
		self.schem.tags.append(TAG_Int_Array(name="Offset"));
		self.schem["Offset"].value = [];
		self.schem["Offset"].value.extend([0, 0, 0]);

		#Metadata: contains world edit offset and world edit version data (simply initialize this)
		#for modification later
		metadata = TAG_Compound(name = "Metadata");
		if(self.plane == "xy"):
			metadata["WEOffsetX"] = TAG_Int(name="WEOffsetX", value = 0);
			metadata["WEOffsetY"] = TAG_Int(name="WEOffsetY", value = 0);
			metadata["WEOffsetZ"] = TAG_Int(name="WEOffsetZ", value = 1);
		else:
			metadata["WEOffsetX"] = TAG_Int(name="WEOffsetX", value = 1);
			metadata["WEOffsetY"] = TAG_Int(name="WEOffsetY", value = 0);
			metadata["WEOffsetZ"] = TAG_Int(name="WEOffsetZ", value = 0);
		metadata["FAWEVersion"] = TAG_Int(name="FAWEVersion", value = 0);
		self.schem.tags.append(metadata);

		#Palette: contains the block palette
		self.schem.tags.append(TAG_Int(name = "PaletteMax", value = len(self.block_palette)));
		palette = TAG_Compound(name = "Palette");
		p_index = 0;
		for block in self.block_palette:
			palette[block] = TAG_Int(name=block, value = p_index);
			p_index += 1;

		self.schem.tags.append(palette);

		#Block data: contains the schematic's block data in a byte array
		self.schem.tags.append(TAG_Byte_Array(name="BlockData"));
		self.schem["BlockData"].value = [];
		data = bytearray(self.block_data);
		self.schem["BlockData"].extend(data);

		#Useless block entitities
		self.schem.tags.append(TAG_List(name="BlockEntities", type=TAG_Compound));

		#Useless entities
		self.schem.tags.append(TAG_List(name="Entities", type=TAG_Compound));

		print(self.schem.pretty_tree());


	#function returns a blockname based off from a colorcode and the provided palette (NOTE: north=+z south =-z)
	def GetBlockName(self, rgb):
		initial_string = "minecraft:"
		match rgb:
			#wall left
			case (255, 0, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=none,south=none,up=false,waterlogged=false,west=tall]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=none,south=none,up=false,waterlogged=false,west=none]";
				else:
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=tall,south=none,up=false,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=none,south=tall,up=false,waterlogged=false,west=none]";
			#wall center
			case (0, 255, 0):
				return "minecraft:mud_brick_wall[east=false,north=none,south=tall,up=true,waterlogged=false,west=none]";
			#wall right
			case (0, 0, 255):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=tall,north=none,south=none,up=false,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=none,north=none,south=none,up=false,waterlogged=false,west=tall]";
				else:
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=none,south=tall,up=false,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=tall,south=none,up=false,waterlogged=false,west=none]";
			#wallpost left
			case (255, 255, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=tall]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=none,south=none,up=true,waterlogged=false,west=none]";
				else:
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=tall,south=none,up=true,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=none,south=tall,up=true,waterlogged=false,west=none]";
			#wallpost right
			case (0, 255, 255):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=tall,north=none,south=none,up=true,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=tall]";
				else:
					if(not self.flip_u):
						return "minecraft:mud_brick_wall[east=none,north=none,south=tall,up=true,waterlogged=false,west=none]";
					else:
						return "minecraft:mud_brick_wall[east=tall,north=tall,south=none,up=true,waterlogged=false,west=none]";
			#trapdoor
			#left
			case (0, 0, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_trapdoor[facing=east,half=top,open=true,powered=false,waterlogged=false]";
					else:
						return "minecraft:jungle_trapdoor[facing=west,half=top,open=true,powered=false,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_trapdoor[facing=north,half=top,open=true,powered=false,waterlogged=false]";
					else:
						return "minecraft:jungle_trapdoor[facing=south,half=top,open=true,powered=false,waterlogged=false]";
			#right
			case (255, 255, 255):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_trapdoor[facing=west,half=top,open=true,powered=false,waterlogged=false]";
					else:
						return "minecraft:jungle_trapdoor[facing=east,half=top,open=true,powered=false,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_trapdoor[facing=south,half=top,open=true,powered=false,waterlogged=false]";
					else:
						return "minecraft:jungle_trapdoor[facing=north,half=top,open=true,powered=false,waterlogged=false]";
			#top
			case (255, 0, 255):
				return "minecraft:jungle_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false]";
			#bottom
			case (127, 0, 255):
				return "minecraft:jungle_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false]";
			#stairs
			#type j
			case (0, 127, 255):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]";
			#type l
			case (0, 255, 127):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]";
			#type 7
			case (127, 255, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=east,half=top,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=west,half=top,shape=straight,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=south,half=top,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=north,half=top,shape=straight,waterlogged=false]";
			#type r
			case (255, 127, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=west,half=top,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=east,half=top,shape=straight,waterlogged=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_stairs[facing=north,half=top,shape=straight,waterlogged=false]";
					else:
						return "minecraft:jungle_stairs[facing=south,half=top,shape=straight,waterlogged=false]";
			#fence closed
			#top
			case (255, 0, 127):
				if(self.plane == "xy"):
					return "minecraft:jungle_fence_gate[facing=north,in_wall=false,open=false,powered=false]";
				else:
					return "minecraft:jungle_fence_gate[facing=east,in_wall=false,open=false,powered=false]";
			#mid
			case (127, 0, 0):
				if(self.plane == "xy"):
					return "minecraft:jungle_fence_gate[facing=north,in_wall=true,open=false,powered=false]";
				else:
					return "minecraft:jungle_fence_gate[facing=east,in_wall=true,open=false,powered=false]";
			#fence opened
			#topleft
			case (127, 127, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=west,in_wall=false,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=east,in_wall=false,open=true,powered=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=south,in_wall=false,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=north,in_wall=false,open=true,powered=false]";
			#midleft
			case (0, 127, 0):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=west,in_wall=true,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=east,in_wall=true,open=true,powered=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=south,in_wall=true,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=north,in_wall=true,open=true,powered=false]";
			#topright
			case (0, 127, 127):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=east,in_wall=false,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=west,in_wall=false,open=true,powered=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=north,in_wall=false,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=south,in_wall=false,open=true,powered=false]";
			#midright
			case (0, 0, 127):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=west,in_wall=true,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=east,in_wall=true,open=true,powered=false]";
				else:
					if(not self.flip_u):
						return "minecraft:jungle_fence_gate[facing=south,in_wall=true,open=true,powered=false]";
					else:
						return "minecraft:jungle_fence_gate[facing=north,in_wall=true,open=true,powered=false]";
			#piston
			#top
			case(127, 0, 127):
				return "minecraft:piston_head[facing=up,short=false,type=normal]";
			#right
			case(127, 127, 127):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:piston_head[facing=east,short=false,type=normal]";
					else:
						return "minecraft:piston_head[facing=west,short=false,type=normal]";
				else:
					if(not self.flip_u):
						return "minecraft:piston_head[facing=north,short=false,type=normal]";
					else:
						return "minecraft:piston_head[facing=south,short=false,type=normal]";
			#down
			case(62, 0, 127):
				return "minecraft:piston_head[facing=down,short=false,type=normal]";
			#left
			case(127, 0, 62):
				if(self.plane == "xy"):
					if(not self.flip_u):
						return "minecraft:piston_head[facing=west,short=false,type=normal]";
					else:
						return "minecraft:piston_head[facing=north,short=false,type=normal]";
				else:
					if(not self.flip_u):
						return "minecraft:piston_head[facing=south,short=false,type=normal]";
					else:
						return "minecraft:piston_head[facing=north,short=false,type=normal]";
			#slab
			#top
			case(189, 189, 189):
				return "minecraft:jungle_slab[type=top,waterlogged=false]";
			#bottom
			case(62, 62, 62):
				return "minecraft:jungle_slab[type=bottom,waterlogged=false]";
			#fullblock
			case(0, 62, 0):
				return "minecraft:jungle_planks";
			#airblock
			case(190, 255, 255):
				return "minecraft:air";

	#processes the actual color data into blocks to be outputted and the creation of a palette
	def ProcessImage(self):
		#first read through the image data to store block id and 2D positional data
		width = self.image_data.width;
		height = self.image_data.height;

		t_palette = [];
		t_block_data = [];

		for y in range(0, height):
			for x in range(0, height):
				block_name = self.GetBlockName(self.image_data.getpixel((x, y)));

				#first handle precaching the palette blocks by seeing if a block is already in the palette, if not add it
				palette_index = len(t_palette)

				if (block_name not in t_palette):
					t_palette.append(block_name);
				else:
					palette_index = t_palette.index(block_name);

				#next add the block index to a list of blocks along with it's 2D location
				true_y = height - 1 - y;

				block_coords = (0, 0, 0);
				if(self.plane == "xy"):
					if(not self.flip_u):
						block_coords = (x, true_y, 0);
					else:
						block_coords = (width - 1 - x, true_y, 0);
				else:
					if(not self.flip_u):
						block_coords = (0, true_y, x);
					else:
						block_coords = (0, true_y, width - 1 - x);

				block_info = (palette_index, block_coords);
				t_block_data.append(block_info);

		#append temporary list to this class's block palette
		for block in t_palette:
			self.block_palette.append(block);

		#finally sort the block data by height then length then width
		t_block_data.sort(key=GetKeyBlockDataWidth);
		t_block_data.sort(key=GetKeyBlockDataLength);
		t_block_data.sort(key=GetKeyBlockDataHeight);

		for block in t_block_data:
			self.block_data.append(block[0]);