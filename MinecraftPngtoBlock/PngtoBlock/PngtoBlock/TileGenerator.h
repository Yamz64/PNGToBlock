#ifndef _GENERATOR_H_
#define _GENERATOR_H_
#include "Tiles.h"

#include <string>
#include <algorithm>
#include <iostream>

//helper class for storing tiles and their pixelmatch score in the tile generator
class TileKV {
public:
	//CONSTRUCTOR/DESTRUCTOR
	TileKV(Tile* tile) { m_tile = tile; m_score = 0; }
	//~TileKV() { std::cout << "Destroying:" << m_tile->GetName() << std::endl;  delete m_tile; }

	//SETTERS
	void SetScore(int score) { m_score = score; }

	//ACCESSORS
	Tile GetTile() { return *m_tile; }
	Tile* GetTilePointer() { return m_tile; }
	unsigned int GetScore() { return m_score; }

	//SORTING OVERLOAD
	friend bool operator<(TileKV a, TileKV b) {
		if (a.m_score < b.m_score) return true;
		if (a.m_score > b.m_score) return false;
		if (a.m_tile->GetName() < b.m_tile->GetName()) return true;
		if (a.m_tile->GetName() > b.m_tile->GetName()) return false;
		return true;
	}
	
private:
	Tile* m_tile;
	int m_score;
};

//class for creation of colorcoded tile data from .png
class TileGenerator {
public:
	//CONSTRUCTOR
	TileGenerator(std::string input_path, std::string output_path);
	~TileGenerator();

	//MISC
	void LoadPNG(std::string file_path);
	void WritePNG(std::string file_path);
	void LoadTiles();
	void AnalyzeSector(int x, int y);
	void AnalyzeImage();

private:
	int m_width, m_height, m_channels;
	unsigned char* m_input_image;
	std::vector<TileKV> m_tile_priority;
	std::vector<unsigned int*> m_outputted_colors;
};
#endif