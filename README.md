# NovaBlitz API

A restful JSON API for the cards in the [NovaBlitz card game](https://novablitz.com/).

Live on PythonAnywhere [here](http://novablitz.pythonanywhere.com/cards/acolyteofhalos).

## Usage

Clone this repository:

```bash
$ git clone https://github.com/kajchang/NovaBlitz.git
$ cd NovaBlitz
```

Assemble the latest card data in `json` format by scraping the NovaBlitz wiki (this will take around a minute):

```bash
$ python3 scraper.py
```

Run the Flask server:

```bash
$ python3 api.py
```

Test it out:

```bash
$ curl localhost:5000/cards/acolyteofhalos

{
    "set": "Base Set", 
    "name": "Acolyte of Halos", 
    "text": "When you summon an Angel, this gets +3 Health.", 
    "image": "https://d1u5p3l4wpay3k.cloudfront.net/novablitz_gamepedia/thumb/4/48/Acolyte_of_Halos%28101048%29.png/200px-Acolyte_of_Halos%28101048%29.png?version=81701fdf268c1d134a050fd322bcee3e", 
    "rarity": "Common", 
    "subtype": "Priest", 
    "attack": 5, 
    "cost": 2, 
    "health": 5, 
    "aspect": "Divine", 
    "type": "Unit"
}
```

## Endpoints

`cards/card_name`

Returns information on the card.

Example: [http://novablitz.pythonanywhere.com/cards/acolyteofhalos](http://novablitz.pythonanywhere.com/cards/acolyteofhalos)

`cardlist`

Returns a list of the names of every card.

Example: [http://novablitz.pythonanywhere.com/cardlist](http://novablitz.pythonanywhere.com/cardlist)

`cards?cards[]=card_name1&cards[]=card_name2`

The same as the `cards/card_name` endpoint, but for searching for multiple cards in one request.

Example: [http://novablitz.pythonanywhere.com/cards?cards[]=FairySentry&cards[]=FlayedDemon&cards[]=AcolyteOfHalos](http://novablitz.pythonanywhere.com/cards?cards[]=FairySentry&cards[]=FlayedDemon&cards[]=AcolyteOfHalos)
