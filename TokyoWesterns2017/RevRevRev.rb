# アドレス 0x8048870 に入っている値
bytes = [0x41,0x29,0xd9,0x65,0xa1,0xf1,0xe1,0xc9,0x19,0x09,0x93,0x13,0xa1,0x09,0xb9,0x49,0xb9,0x89,0xdd,0x61,0x31,0x69,0xa1,0xf1,0x71,0x21,0x9d,0xd5,0x3d,0x15,0xd5]

puts(bytes.map do |b|
	b ^= 0xFF
	b.to_s(2).rjust(8, '0').reverse.to_i(2).chr
end.join.reverse)