
require 'pty'
require 'expect'

$expect_verbose=true

PTY.spawn("./121-calculation") do |r,w|
	w.sync = true
	while true
		r.expect(/^(.+) = /, 5) do |match|
			input = match[0]
			input[-2, 2] = ''
			result = eval(input)
			w.puts(result)
		end
	end
end

