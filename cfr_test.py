from cfr_player import CFRPlayer

cfr = CFRPlayer()
util = cfr.train(1000000)

print "Player One Expected Value Per Hand: %f" % util

result = cfr.get_betting_frequencies()

for decision in sorted(result):
    print decision
    output = ""
    for card in sorted(result[decision]):
        output += str(card) + ": " + str(result[decision][card]) + ",   "

    print output + "\n"
