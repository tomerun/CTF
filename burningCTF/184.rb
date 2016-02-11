require 'open3'

dummy_name = '_'
while true
	filename = Dir.glob('*').reject {|f| f == $0}[0]
	puts "filename:#{filename}"
	type = ''
	Open3.popen2("file #{filename}") do |_, out, _|
		type = out.gets
	end
	puts type 
	File.rename(filename, dummy_name)
	if type.include?('bzip2')
		system("bzip2 -d #{dummy_name}")
	elsif type.include?('tar archive')
		system("tar -xvzf #{dummy_name}")
	elsif type.include?('Zip archive')
		system("unzip #{dummy_name}")
	elsif type.include?('gzip compressed data')
		File.rename(dummy_name, dummy_name + '.gz')
		system("gunzip #{dummy_name}.gz")
	else
		break
	end
	File.delete(dummy_name) if Dir.glob('*').size == 3 && File.exist?(dummy_name)
end
