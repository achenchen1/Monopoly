# How can we provide a simple interface for multiple players to play a game of Monopoly?

Just brainstorming ideas

## 1/18/2024

Idea:

1. Server generates a public key, on an invite link - the same invite link can be used for all invited players

2. Player encrypts a hash with the public key, e.g. a hashed (very insecure) password.

3. In the future, all mutating actions (buying, selling, trading, etc. - does not include listing the properties) must have this password prepended or appended - e.g. maybe the packet looks like Public Key("buy, baltic avenue, foo_bar_password")
