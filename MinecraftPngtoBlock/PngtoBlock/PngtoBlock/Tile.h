#ifndef _TILE_H_
#define _TILE_H_
#include <vector>

class Tile {
protected:
	//SETTER
	void ApplyColor(unsigned int color[3]) {
		m_color[0] = color[0];
		m_color[1] = color[1];
		m_color[2] = color[2];
	}

	void ApplyData(std::vector<std::vector<bool>>& data) {
		for (unsigned int i = 0; i < data.size(); i++) {
			std::vector<bool> temp = std::vector<bool>(data[i]);
			m_tiledata.push_back(temp);
		}
	}

	void SetName(const char* name) { m_name = name; }

public:
	Tile() {}

	//Copy constructor
	Tile(Tile& t) {
		ApplyColor(t.m_color);
		ApplyData(t.m_tiledata);
		m_name = t.m_name;
	}

	//Accessor
	const bool GetPixel(int x, int y) { return m_tiledata[x][y]; }
	const char* GetName() { return m_name; }
	unsigned int* GetColor() { return m_color; }

private:
	std::vector<std::vector<bool>> m_tiledata;
	unsigned int m_color[3];
	const char* m_name;
};
#endif
