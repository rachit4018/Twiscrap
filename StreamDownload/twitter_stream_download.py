import tweepy
from tweepy import OAuthHandler
import time
import argparse
import string
import config
from tweepy import StreamingClient
def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


def on_data(data):
    try:
        with open(outfile, 'a') as f:
            f.write(data)
            print(data)
            return True
    except BaseException as e:
        print("Error on_data: %s" % str(e))
        time.sleep(5)
    return True

def on_error(status):
    print(status)
    return True

def format_filename(fname):
    """Convert file name into a safe string.

    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)

def convert_valid(one_char):
    """Convert a character into '_' if invalid.

    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAP0crQEAAAAA%2BTQ3Tui49vIZ24gqSiCfL4JgIjA%3DwXtTMO2hvkmZqg7FMi94zsxsepL2gtTb15BGHaUH7preGI7RPI")
    #auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    #auth.set_access_token(config.access_token, config.access_secret)

    query_fname = format_filename(args.query)
    outfile = "%s/stream_%s.json" % (args.data_dir, query_fname)
    client = StreamingClient(tweepy.api.auth)
   
    client.on_data = on_data
    client.on_error = on_error
    client.sample()
    client.add_rules(tweepy.StreamRule("Tweepy"))
    #client.filter()