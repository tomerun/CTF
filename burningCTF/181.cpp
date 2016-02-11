#include <string>
#include <iostream>
#include <unordered_map>

using namespace std;

const uint64_t P = 17;
int N;
string str;

int ok(int L) {
	uint64_t hash = 0;
	uint64_t last = 1;
	for (int i = 0; i < L; ++i) {
		hash *= P;
		hash += str[i];
		last *= P;
	}
	unordered_map<uint64_t, int> map;
	map[hash] = 0;
	for (int i = L; i < N; ++i) {
		hash *= P;
		hash += str[i];
		hash -= str[i - L] * last;
		if (map.find(hash) != map.end()) return map[hash];
		map[hash] = i - L + 1;
	}
	return -1;
}

int main() {
	cin >> str;
	N = str.size();
	int lo = 1;
	int hi = N;
	while (hi - lo > 1) {
		int mid = (lo + hi) / 2;
		int pos = ok(mid);
		if (pos >= 0) {
			lo = mid;
		} else {
			hi = mid;
		}
	}
	int pos = ok(lo);
	cout << string(str.begin() + pos, str.begin() + pos + lo) << endl;
}