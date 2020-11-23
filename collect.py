import requests
import argparse
import json
import os.path as osp



def main():
	print(3)
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', help='The output file containing the reddit posts. Must be of the form <yyyy><mm><dd>_politics.json')
	args = parser.parse_args()
	output_file = args.o
	output_clean = open(osp.join('data',f'{output_file}_clean.json'),'w')
	output_raw = open(osp.join('data',f'{output_file}_raw.json'),'w')


	for post in get_posts('/r/conservative',output_raw):
		json.dump(post,output_clean,indent=4)
		output_clean.write('\n')

def get_posts(subreddit,output_raw):
	list = []
	after=''
	gather = True
	while(gather):
		data = requests.get(f'http://api.reddit.com{subreddit}/new?limit=100&after={after}',headers={'User-Agent':'osx: requests (by /u/dpmurray21)'})
		content_list = data.json()['data']['children']
		if(len(content_list) == 0):
			return list
		after = content_list[len(content_list) - 1]['data']['name']
		for post in content_list:
			reddit_post = post['data']
			if biden_trump_mentioned(reddit_post) != 0 :
				if len(list) <= 333:
					json.dump(post,output_raw)
					output_raw.write('\n')
					list.append(create_output_dict(reddit_post))
				else:
					gather= False

	return list


def create_output_dict(reddit_post):
	dictionary = dict()
	dictionary['content'] = reddit_post['selftext']
	dictionary['title'] = reddit_post['title']
	dictionary['name'] = reddit_post['name']
	dictionary['gildings'] = reddit_post['gildings']
	dictionary['up_votes'] = reddit_post['ups']
	dictionary['down_votes'] = reddit_post['downs']
	if 'url_overridden_by_dest' in reddit_post:
		dictionary['associated_url'] = reddit_post['url_overridden_by_dest']

	return dictionary

def biden_trump_mentioned(reddit_post):
	trump_count = reddit_post['title'].count('Trump') + reddit_post['selftext'].count('Trump')
	biden_count = reddit_post['title'].count('Biden') + reddit_post['selftext'].count('Biden')
	return (trump_count + biden_count) != 0

if __name__ == '__main__':
	main()

















