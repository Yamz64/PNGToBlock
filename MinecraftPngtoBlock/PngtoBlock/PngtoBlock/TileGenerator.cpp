#include "TileGenerator.h"

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include <stb_image_write.h>

#include <iostream>
#include <chrono>

//helper function so that the output isn't ugly
float Round(float f) {
	float value = (int)(f * 100 + 0.5);
	return (float)value / 100;
}

//The constructor will automatically output an image from an inputted image
TileGenerator::TileGenerator(std::string input_path, std::string output_path) {
	LoadPNG(input_path);
	LoadTiles();

	//keep track of the time it takes to analyze the image
	std::cout << "Analyzing image..." << std::endl;
	std::chrono::time_point<std::chrono::system_clock> start, end;
	start = std::chrono::system_clock::now();

	AnalyzeImage();

	end = std::chrono::system_clock::now();
	
	std::chrono::duration<double> elapsed_seconds = end - start;

	std::cout << "Analysis finished in: " << elapsed_seconds.count() << " seconds" << std::endl;

	WritePNG(output_path);
	stbi_image_free(m_input_image);
}

TileGenerator::~TileGenerator() {
	//first clear up all allocated colors
	for (unsigned int i = 0; i < m_outputted_colors.size(); i++) {
		delete[] m_outputted_colors[i];
	}

	//then clear up the priority list
	for (unsigned int i = 0; i < m_tile_priority.size(); i++) {
		delete m_tile_priority[i].GetTilePointer();
	}
}

//function loads a png from a specified filepath
void TileGenerator::LoadPNG(std::string file_path) {
	m_input_image = stbi_load(file_path.c_str(), &m_width, &m_height, &m_channels, 0);
}

//function writes to png at selected filepath from m_outputted_colors
void TileGenerator::WritePNG(std::string file_path) {
	//prepare a cache of bytes to write to
	const int capacity = m_outputted_colors.size() * m_channels;
	unsigned char* o_image = new unsigned char[capacity];

	for (unsigned int i = 0; i < m_outputted_colors.size(); i++) {
		o_image[i*3] = (uint8_t)(m_outputted_colors[i][0]);
		o_image[i*3 + 1] = (uint8_t)(m_outputted_colors[i][1]);
		o_image[i*3 + 2] = (uint8_t)(m_outputted_colors[i][2]);
	}

	//write cache to a .png
	stbi_write_png(file_path.c_str(), m_width / 16, m_height / 16, m_channels, o_image, (m_width / 16) * m_channels);
	delete[] o_image;
}

//function will load all tiles for use later
void TileGenerator::LoadTiles() {
	//initialize pointers to a bunch of tiles
	//walls
	TileKV wall_left = TileKV(new Wall_LEFT());
	TileKV wall_right = TileKV(new Wall_RIGHT());
	TileKV wall_center = TileKV(new Wall_CENTER());

	//wallposts
	TileKV wall_post_left = TileKV(new Wall_Post_LEFT());
	TileKV wall_post_right = TileKV(new Wall_Post_RIGHT());

	//trapdoors
	TileKV trapdoor_left = TileKV(new Trapdoor_LEFT());
	TileKV trapdoor_right = TileKV(new Trapdoor_RIGHT());
	TileKV trapdoor_top = TileKV(new Trapdoor_TOP());
	TileKV trapdoor_bottom = TileKV(new Trapdoor_BOTTOM());

	//stairs
	TileKV stair_typej = TileKV(new Stair_TYPEJ());
	TileKV stair_typel = TileKV(new Stair_TYPEL());
	TileKV stair_type7 = TileKV(new Stair_TYPE7());
	TileKV stair_typer = TileKV(new Stair_TYPER());

	//fence closed
	TileKV fence_closed_top = TileKV(new Fence_Closed_TOP());
	TileKV fence_closed_mid = TileKV(new Fence_Closed_MID());

	//fence opened
	TileKV fence_topleft = TileKV(new Fence_TOPLEFT());
	TileKV fence_midleft = TileKV(new Fence_MIDLEFT());
	TileKV fence_topright = TileKV(new Fence_TOPRIGHT());
	TileKV fence_midright = TileKV(new Fence_MIDRIGHT());

	//piston
	TileKV piston_top = TileKV(new Piston_TOP());
	TileKV piston_right = TileKV(new Piston_RIGHT());
	TileKV piston_down = TileKV(new Piston_DOWN());
	TileKV piston_left = TileKV(new Piston_LEFT());

	//slab
	TileKV slab_top = TileKV(new Slab_TOP());
	TileKV slab_bottom = TileKV(new Slab_BOTTOM());

	//full block
	TileKV full_block = TileKV(new FullBlock());

	//air block
	TileKV air_block = TileKV(new AirBlock());

	//store all tile key value pairs into the priority vector
	m_tile_priority.insert(m_tile_priority.end(), {
		wall_left, wall_right, wall_center,
		wall_post_left, wall_post_right,
		trapdoor_left, trapdoor_right, trapdoor_top, trapdoor_bottom,
		stair_typej, stair_typel, stair_type7, stair_typer,
		fence_closed_top, fence_closed_mid,
		fence_topleft, fence_midleft, fence_topright, fence_midright,
		piston_top, piston_right, piston_down, piston_left,
		slab_top, slab_bottom,
		full_block,
		air_block
	});
}

//function handles comparing an entire sector's worth of pixels with existing tiledata
void TileGenerator::AnalyzeSector(int x, int y) {
	//reset the score of all tiles
	for (unsigned int i = 0; i < m_tile_priority.size(); i++) {
		m_tile_priority[i].SetScore(0);
	}

	//loop through the entire sector and adjust score for each tile
	unsigned int sector_offset = (y * m_width + x) * m_channels;
	for (unsigned int r = 0; r < 16; r++) {
		for (unsigned int c = 0; c < 16; c++) {
			//png image
			unsigned int pixel_offset = (r * m_width + c) * m_channels;

			int pixel_color[3] = {
				static_cast<int>(m_input_image[sector_offset + pixel_offset]),
				static_cast<int>(m_input_image[sector_offset + pixel_offset + 1]),
				static_cast<int>(m_input_image[sector_offset + pixel_offset + 2])
			};

			//loop through the entire tile priority list and compare pixel locations for each tile
			for (unsigned int i = 0; i < m_tile_priority.size(); i++) {

				//if the tile believes a pixel should be in a location...
				if (m_tile_priority[i].GetTile().GetPixel(r, c)) {
					//increment score if it is correct
					if (pixel_color[0] == 0 && pixel_color[1] == 0 && pixel_color[2] == 0)
						m_tile_priority[i].SetScore(m_tile_priority[i].GetScore() + 1);
					//decrement score if it is wrong
					else
						m_tile_priority[i].SetScore(m_tile_priority[i].GetScore() - 1);
				}
			}
		}
	}

	//sort the tile priority list, and assign the best tile's color to the outputted colors
	std::sort(m_tile_priority.rbegin(), m_tile_priority.rend());
	unsigned int* rgb = new unsigned int[3];
	rgb[0] = m_tile_priority[0].GetTile().GetColor()[0];
	rgb[1] = m_tile_priority[0].GetTile().GetColor()[1];
	rgb[2] = m_tile_priority[0].GetTile().GetColor()[2];
	m_outputted_colors.push_back(rgb);

	float completion_percent = (float)(x + y*m_width) / (float)(m_width * m_height);
	completion_percent *= 100.0f;

	std::cout << Round(completion_percent) << "%\tSector at: (" << x << ", " << y << "),\tBlock chosen: "
		<< m_tile_priority[0].GetTile().GetName() << std::endl;
}

//function handles analyzing the entire image and storing color coded tiles into m_outputted_colors
void TileGenerator::AnalyzeImage() {

	//loop through the entire image in increments of 16, to get the starting coordinate of each sector
	for (unsigned int y = 0; y < m_height; y += 16) {
		for (unsigned int x = 0; x < m_width; x += 16) {
			AnalyzeSector(x, y);
		}
	}
}
