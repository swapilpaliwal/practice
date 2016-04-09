
# coding: utf-8

# In[ ]:

# importing necessary packages
import json
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import os.path as op
import os

datapath = op.join(os.getcwd(),'../coding-challenge/src/')


# Declaring important variables
arr_tweets_hashtags = []
arr_tweet_time = []
time_arr_1_or_more_hashtags = []
arr_hashtags_1_or_more_hashtags = []
array_of_sequence = []
arr = []
arr_of_rolling_avg = []

def capture_total_tweets_and_make_arrays(filename='tweet_input/tweets.txt'):
    """
    Function: Takes a tweet file with filename as input and generates 
              arrays that can be used for further analysis.
              
              The functions takes advantage of JSON architecture of 
              tweets and segregates tweets with rate limiting messages.
              
    Input: Filename of tweet file [ example : ('tweets.txt') ]
    Output: Returns total lines in the text file and number of tweets
            also creates the arrays containing hashtags and time stamps 
            for further processing.
    """
    total_lines_in_file = 0
    with open(filename, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            total_lines_in_file +=1
            
            # To segregate the tweets with rate limiting messages 
            # which do not have created_at keys
            try :
                all_hashtags_in_tweet = []
                time_stamp = tweet['created_at']
                (arr_tweet_time.append(datetime.strptime(
                        time_stamp, '%a %b %d %H:%M:%S +0000 %Y')))
                entities = tweet['entities']
                for hashtags in entities['hashtags']:
                    all_hashtags_in_tweet.append(hashtags['text'])
                arr_tweets_hashtags.append(all_hashtags_in_tweet)
            except:
                pass
    print 'total lines in file: ', total_lines_in_file
    print 'Total number of tweets: ', len(arr_tweet_time)


def collect_tweets_with_1_or_more_hashtags():
    """
    Function: It filters out tweets with no hashtags and returns tweets 
              with atleast one hashtag for further processing.  
    Input:    None
    Output:   None (Its only generating array to filter tweets with no hashtags)
    """
    capture_total_tweets_and_make_arrays()
    for i,j,k in (zip(xrange(len(arr_tweet_time)),arr_tweet_time, 
                      arr_tweets_hashtags)):
            try :
                if k[0]:
                    time_arr_1_or_more_hashtags.append(j)
                    arr_hashtags_1_or_more_hashtags.append(k)
                    array_of_sequence.append(i)
            except:
                pass
    for i, j , k, m in  (zip (xrange(len(arr_hashtags_1_or_more_hashtags)), 
                              time_arr_1_or_more_hashtags, 
                              arr_hashtags_1_or_more_hashtags,
                              array_of_sequence)):
        arr.append((i,j,k,m))

def generate_edges(graph):
    """
    Function: Takes in dictionary objects "graph" and generates edges.
    Input   : dictionary containing vertices (vertex1 : vertex2 ==> key : value)
    Output  : generates edges from the hastags vertices
    """
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    return edges    


def calculate_rolling_degree():
    """
    Function : Takes in all tweets with atleast one hashtag one by one
               and applies one minute rule and logic to create rolling
               average. 
    Input :    None
    Output :   Generates the average rolling degree for tweets with atleast 
               two hashtags, but considers all tweets with atleast one hashtag
               to apply the time constraint logic of one minute. 
    
    """
    count = 0
    extras = 0
    base_time = arr[0][1]
    for j in xrange(len(arr)):
        time = arr[j][1]
        hashtag_arr = arr[j][2]
        m = arr[j][3]                       
        if time >= base_time :
            base_time = time
            extras = 0
        if time != base_time:
            count += 1
            extras += 1
        edges = []
        for k in xrange(j+1 + extras):
            try:
                time_new = arr[k][1]
                hashtag_arr_new = arr[k][2]
                if (base_time - time_new).total_seconds() <= 60:
                    linked_dict = {}
                    new_array = []

                    for i in xrange(len(hashtag_arr_new)): 
                        linked_dict[hashtag_arr_new[i]] = [hashtag_arr_new[:i]]
                        linked_dict[hashtag_arr_new[i]].append(hashtag_arr_new[i+1:])
                        linked_dict[hashtag_arr_new[i]] = sum(linked_dict[hashtag_arr_new[i]],[])
                    new_array.append(linked_dict)

                    for dicts in new_array:
                        edges.append(generate_edges(dicts))
                    combined_list_of_edges = sum(edges,[])

                    dict_of_vertex = defaultdict(list)
                    for k,v in combined_list_of_edges:
                        if v not in dict_of_vertex[k]:
                            dict_of_vertex[k].append(v)

                    degree = []
                    for key, values in dict_of_vertex.iteritems():
                        degree.append(len(values))

                    rolling_degree = 0
                    rolling_degree = "{0:.2f}".format(float(sum(degree))/len(degree)) 
            
            except:
                pass
            
        arr_of_rolling_avg.append([m, rolling_degree]) 


        
def generate_rolling_degree_output():
    """
    Function : writes the rolling degree for all tweets into outputs.txt 
               it including tweets which do not contain any hashtags.
    Input :    NONE
    Output :   generates the output.txt file which contains the rolling averages.
    """
    p = np.zeros((len(arr_tweet_time),2))
    for i,j in arr_of_rolling_avg:
        p[i]=i,j
    for m in xrange(len(p)):
        if p[m].all() == 0:
            p[m] = m, p[m-1][1]
    with open('tweet_output/output.txt', 'w') as f:
        for m,n in p:
            f.write(str(n) + '\n')
            
            
collect_tweets_with_1_or_more_hashtags()
calculate_rolling_degree()
generate_rolling_degree_output()

