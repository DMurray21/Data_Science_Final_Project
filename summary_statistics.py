import argparse
import json
from electiontopics import utils
import matplotlib.pyplot as plt
import os.path as osp
import pandas as pd

def main():

    # Setup

    ## Get cmdline args
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath", help="path to data")
    parser.add_argument("-p", "--plots", help="the path to store plots, if desired")
    args = parser.parse_args()

    ## Load data
    data = utils.load_data(args.datapath)

    ## Convert to dataframe (for ease of use)
    df = utils.data_to_frame(data)

    ## Annotate with source
    df['source'] =df['associated_url'].map(lambda x: utils.extract_domain(x))


    # Get some useful numbers

    num_posts = df.shape[0]
    print(f"Number of posts: {num_posts}")


    # Calculate distribution of topics

    topic_ratios = df['code'].value_counts(normalize=True)

    print("Overall Topic Ratios:")
    print(topic_ratios)
    print()

    # Sources

    ## Most common sources

    source_counts = df['source'].value_counts()
    most_common = [source for source in zip(source_counts.index[:5], source_counts[:5])]
    print(f"The five most common sources in this dataset are {most_common}")
    print()


    ## Topics for common sources

    source_dfs = []
    print('Topic distributions: ')
    for source, count in most_common:
        
        source_df = df[df['source'] == source]['code'].value_counts(normalize=True)
        print(f'for {source}:')
        print(source_df)

        print()

        source_dfs.append((source, source_df, count))

    full_source = pd.DataFrame({(k + " (n=" + str(c) + ")"):v for k,v,c in source_dfs})

    # Plot

    if args.plots is not None:

        plt.clf()

        topic_ratios.plot(kind='bar')
        plt.tight_layout()
        plt.savefig(osp.join(args.plots, 'topic ratios.png'))
        plt.clf()

        ax = full_source.plot(kind='bar')
        ax.set_ylabel("Topic Ratio")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(osp.join(args.plots, 'source topic ratios.png'), bbox_extra_artists=(legend,))
        plt.clf()



if __name__ == "__main__":
    main()