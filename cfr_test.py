from cfr_player import CFRPlayer

cfr = CFRPlayer()
util = cfr.train(3000000)

print "Player One Expected Value Per Hand: %f" % util

result = cfr.get_betting_frequencies()

for decision in sorted(result):
    print decision
    output = ""
    for card in sorted(result[decision]):
        temp = card + 2
        card_name = str(temp)
        if temp == 10:
            card_name = 'T'
        elif temp == 11:
            card_name = 'J'
        elif temp == 12:
            card_name = 'Q'
        elif temp == 13:
            card_name = 'K'
        elif temp == 14:
            card_name = 'A'

        output += card_name + ": " + str( round(result[decision][card], 4) ) + ",   "

    print output + "\n"
