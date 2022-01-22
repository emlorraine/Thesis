from retrieve import pull_reddit_data, pull_facebook_data, pull_twitter_data

def determine_sample_size(raw_data_size):
    # confidence level of 95%
    p = 0.05 
    z_score = 1.96	
    std = .5
    margin_of_error = .05
    sample_size = (pow(1.96, 2) * std * (1-std))/(pow(margin_of_error,2))
    return round(sample_size)
