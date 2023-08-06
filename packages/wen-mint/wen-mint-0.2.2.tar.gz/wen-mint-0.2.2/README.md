# Wen Mint

A handy command line tool to scrape Ethereum addresses from your comment threads for more efficient giveaways.

## Social networks supported

Currently this tool works with:
* Reddit
* Twitter
* Other networks if you are able to extract CSVs of comments

## Getting started

The easist way to use this tool is to download it from pip.

```bash
pip install wen-mint
```

It requires python 3.10 or later. if that poses problems for older systems there is a dockerfile in the project's root.

To use the scraping tools, you must include api credentials in a config file. This module can help you generate the file (and obtain a Reddit refresh token), but the core tokens must be obtained manually from the each social network used.

* [Reddit client id and secret](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#oauth)
* [Twitter bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens)
* [Ethereum Remote Provider Url](https://web3py.readthedocs.io/en/stable/quickstart.html?highlight=remote%20providers#remote-providers)

## Usage

Provided are a few examples to get you up and running. More extensive documentation can be found in the `--help` menus.
* `wen-mint generate_config --output <WHERETOSAVETHECONFIGFILE> --twitter_bearer_token <YOURTOKEN>` Creates a config file using your Twitter bearer token that can be used for the Twitter address extraction function.
* `wen-mint get_reddit_refresh_token --config_path <LOCATIONOFYOURCONFIGFILE>` Allows you to retrieve a Reddit Refresh token to be used for the Reddit address extraction function. (Requires a config file with filled in values for "Reddit_client_id", "Reddit_client_secret", and "Reddit_redirect_url")
* `wen-mint reddit <REDDITPOSTID> --config_path <LOCATIONOFYOURCONFIGFILE>` Captures ethereum addresses from the post specified and displays them all seperated by a space in the terminal output. (Requires a config file with filled in values for "Reddit_client_id", "Reddit_client_secret", and "Reddit_refresh_token")
* `wen-mint twitter <TWITTERCONVERSATIONID> --config_path <LOCATIONOFYOURCONFIGFILE> --output <FILEPATHTOSAVECSV> --random_sample 20 --uniform_addresses --liked_only` Scrapes a Twitter thread for addresses and exports a csv that contains more details like the post id, username, and the original text. Also converts all ens addresses to their hexadecimal hash equivelents takes a random sample of 20 after excluding participants who did not like the post, removing all duplicates and instances where no address could be found. (Requires a config file with filled in values for "Twitter_bearer_token" and "ethereum_provider_url" [if enabling "--uniform_addresses"])
* `wen-mint csv <LOCATIONOFINPUTCSV> --post_column "Some posts and junk" --low_precision` Extracts all findable ethereum addresses in a csv where the column for the posts has been prenamed "Some posts and junk". Example csv contains newline characters accidentally stripped out so extraction uses a lower precision method that ignores neighboring characters.

## Considerations

Ethereum addresses are extracted using a targeted regex string that eliminates most cases of false positives and false negatives.
* You will want to use the algorithm in most cases, but it will exclude rare instances when an address runs directly on other words without spaces or newlines seperating them.
* A more permissive approach (that increases false positives) is included in the csv option. Use `--low_precision` to find matches regardless of neighboring non-alphanumeric characters.
* If a single comment contains multiple addresses, only the first address is taken.
* If a single user contributes multiple comments with different addresses only 1 of these (the earliest occuring by id) is taken.

Make sure you convey to your audience to not do wild things to their addresses to ensure that nobody disqualifies themselves by submitting something like "lol😂😂thereisnospaceorlinebreakbetweenmyaddress.eth😂😂😂" Included the repo is example.csv where you can test some of these cases.

## Warning for address lookup and substitution

If connecting to an Ethereum API to change ENS addresses to Ethereum hashes, connecting via a websocket url is currently broken. Connect via http for now instead.

## Having trouble with the Reddit refresh token?

Getting the Reddit refresh token may seem complicated, but it only has to be done once. The key thing to remember is making sure the url on the app you registered (and the port) matches exactly what is in the config file. For example, if you wanted to authenticate locally on port 42069, you would need to have this `http://localhost:42069` for the line that says "redirect uri" for the app on Reddit and also in the config file under "Reddit_redirect_url"

## Need to run without the installed alias?

If you installed the program and are having trouble accessing the alias `wen-min`, you can always access it directly within python with a slight modification to the command. Use `python -m wen_mint.cli`to run it directly.

## One final note

This is a powerful open source tool that leverages other powerful open source tools and is built with the intent of making everyone's lives easier and more efficient. How you use it is your responsibility. Don't be one of those guys that ruins good things for everyone else.
