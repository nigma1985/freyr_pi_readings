import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.getOptions as opt
#import module.freyr.csvBuffer as csv
import module.decision as dec
import os, sys

# _input = sys.argv
# #_input = [0, 'nix', 'out/FREYR_2020-20-00_2599_byangoma.csv', 'test', 'ALLON', 999, 666]
#
# print _input
# csv_name = opt.csvName(options = _input)
#
# all_on = opt.findItm("ALLON")
# all_off = opt.findItm("ALLOFF")
#
# print all_on, all_off, csv_name
#
# print any(["True", False, None])
#
# print any(True)
# print any(None)
# print any("TXT")

#print dec.decision([False, False, False, False], None, 90, 90)

print dec.decision()
