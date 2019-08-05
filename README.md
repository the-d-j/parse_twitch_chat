# Twitch IRC Bot for Giveaways (WIP)
## Built and tested in Python 3.7.2

#### Developed this as an experiment for a specific channel's giveaways.
#### It does the following:

1. Looks for the start of a raffle by detecting raffle entry word/phrase
2. Mitigates false raffle starts by counting number of entries and time elapsed
3. Enters raffle
4. Detects if winner
5. Responds in chat after winning to show "I'm there"
6. After a given time it resets flags/settings to prepare for next raffle     

**Requires:** Twitch OAUTH Token for user, nickname of user, and channel name kept in a local_settings file


This is very basic but future version will be rewritten as OO to account for different channel giveaways.

**Status:** Undergoing testing



