import random

def main():
	files = ['data/20201127_conservative_clean.json'
	,'data/20201128_conservative_clean.json'
	,'data/20201129_conservative_clean.json'
	,'data/20201130_conservative_clean.json'
	, 'data/20201127_politics_clean.json'
	, 'data/20201128_politics_clean.json'
	, 'data/20201129_politics_clean.json']
	
	with open("aggregated_posts.json", "wb") as outfile:
		for f in files:
			with open(f, "rb") as infile:
				outfile.write(infile.read())

	random_line_numbers = random.sample(range(1,1838),200)

	open_coding_file = open("posts_to_code.json",'w')
	aggregated_posts = open("aggregated_posts.json",'r').read().splitlines()
	for line in random_line_numbers:
		open_coding_file.write(aggregated_posts[line])
		open_coding_file.write('\n')






if __name__ == '__main__':
	main()