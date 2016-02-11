#include <string>
#include <iostream>
#include <set>
#include <vector>
#include <array>

using namespace std;

const int H = 10;
const int W = 9;
const vector<int> sorted = {0,1,2,3,4,5,6,7,8,9};
vector<int> ar = {9,8,6,5,7,3,2,1,0,4};

using amida = vector<bool>;
set<amida> ans;

void generate_ans(amida& cur) {
	ans.insert(cur);
	for (int w = 0; w < W; ++w) {
		for (int h = 0; h < H - 1; ++h) {
			if (cur[h * W + w] || cur[(h + 1) * W + w]) continue;
			if (w > 0 && (cur[h * W + w - 1] || cur[(h + 1) * W + w - 1])) continue;
			if (w < W - 1 && (cur[h * W + w + 1] || cur[(h + 1) * W + w + 1])) continue;
			cur[h * W + w] = true;
			cur[(h + 1) * W + w] = true;
			ans.insert(cur);
			cur[h * W + w] = false;
			cur[(h + 1) * W + w] = false;
		}
	}
}

void dfs(int h, int w, amida& cur, int count) {
	if (w >= W) {
		h++;
		w = 0;
	}
	if (h == H) {
		if (ar == sorted) {
			generate_ans(cur);
		}
		return;
	}

	int rest = (H - h - 1) * W + (W - w);
	if (count + (rest + 1) / 2 < 39) return; // prune

	// not use
	dfs(h, w + 1, cur, count);

	// use
	if (h > 0 && cur[(h - 1) * W + w]) return;
	if (ar[w] < ar[w + 1]) return;
	swap(ar[w], ar[w + 1]);
	cur[h * W + w] = true;
	dfs(h, w + 2, cur, count + 1);
	cur[h * W + w] = false;
	swap(ar[w], ar[w + 1]);
}

int main() {
	amida cur(H * W);
	dfs(0, 0, cur, 0);
	cout << ans.size() << endl;

	const string strtes = "qwertyuiopasdfghjklzxcvbnm1234567890_+=";
	array<array<int, 10>, 10> count = {};
	for (const auto& am : ans) {
		for (int i = 0; i < H; ++i) {
			for (int j = 0; j < W; ++j) {
				if (am[i * W + j]) count[i][j]++;
			}
		}
	}
	string result;
	for (int i = 0; i < 10; ++i) {
		for (int j = 0; j < 10; ++j) {
			result += strtes[count[i][j] % strtes.size()];
		}
	}
	cout << result << endl;
}

