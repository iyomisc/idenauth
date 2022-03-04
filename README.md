## What is it?
idenauth is a free Discord bot that links Idena identities with matching Discord roles.
By signing in with an Idena identity, Discord users prove they own a unique identity and its level.

## Why?
Discord is a notorious spammy and low trust place.  
When integrated with Idena, Discord admins make sure to reduce the risk of spam and scams.  
Moreover, they immediately gain a fine grained role structure, from "logged" to "Human", with "newbie" and "verified" in between.  
Since these are Discord roles, they can be used straight away, by giving specific access.

For users, Idena still is fully pseudonymous: no need for real name, no KYC, no personal info ever.


## What is idena?

From the idena team:  
> Idena is a novel way to formalize people on the blockchain. It does not collect or store personally identifiable information. Idena proves the humanness and uniqueness of its participants by running an AI-hard Turing test at the same time for everyone around the globe. The Idena blockchain is driven by proof-of-person consensus: Every node is linked to a cryptoidentity, one single person with equal voting power.
> The Idena validated participants registry is a list of addresses with proven semi-uniqueness of their owners (see examples in the Idena blockchain explorer). Each Idena participant can own one valid cryptoidentity address, it is difficult to have two or more.
> The uniqueness of participants is proven by the fact that they provide answers for flip-puzzles synchronously. A single person is not able to validate herself multiple times because of a very limited timeframe for submission of the answers. The validation status of a participant is not forever. It expires when the next epoch starts. Participants should prolong their validation status for every new epoch. Read more in the Idena website FAQ section.
> https://idena.io/?view=faq

## Discord servers using idenauth

The first server to embed idenauth bot was the Idena Discord.  
The bot got a very warm welcome and was used straight away by many users.  
Discord admin are now thinking of specific channels reserved to the different identity levels.

- Idena Discord https://discord.gg/8BusRj7
- Qortal Project Official Discord Community Server https://discord.com/invite/54UyhB7
- (More to come)

Do you use the bot? please open an issue or PR to be added there.


## Installation

### How to add to my discord server?
Contact Iyomisc on discord or twitter @iyomisc

**Benefits of adding the hosted for you instance:**  
The hosted for you service is free and does not require installation or maintenance from you.  
Invite the bot and it will do its magic and manage the idena roles for you.
Since a single instance runs for all discords, Users signed on one Discord will automatically get the proper role on the others as well.  
At epoch change, the roles will be auto updated with no action from your part.


### How to run a self hosted instance?

Idenauth uses Python3 (min 3.5.3 required) and is based upon discord.py rewrite 
- install the requirements `pip3 install -r requirements.txt`
- create a discord bot, get a token, register and invite (Like any other bot)
- configure the access token in the config `config.json` and start the bot `python3 bot.py`
- configure `config.txt` and start the server `server.py`

Stay informed of updates by watching the github repo or via twitter: @iyomisc


## Idena Hackathon
This project is part of the Idena hackathon https://gitcoin.co/issue/idena-network/idena-go/431/4364

It competes for the "sign in with Idena" bounty.  
- open source code
- uses sign-in with idena and idena app
- definitely provides added value to its users (discord admins and discord users as well)

Idena integration to Discord is a brand new thing and solves some of the issues both Discord users and admin were facing.  
Moreover it adds some competition spirit, pleasure to "flex" some muscle by displaying a "human" identity, and allows for real differentiate services, in a way more realiable manner than what existed before.

This goes beyond the Idena discord itself, since we already are in contact with other discord admins.  
Generic Discords - not directly related to Idena are also likely to integrate this bot, thus making the Idena inovative solution known to a wider audience.

Donation address: 0xf2cc549874f366b66b11eb7bb3ad5a66343ce369

## Licence
MIT licence
