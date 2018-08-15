# import module.netTools as ntt
#
# print ntt.ping_singlehost()
# print ntt.ping_singlehost("0.0.0.0", 5)
#
# print ntt.ping_host()
# print ntt.ping_host(hosts = ["0.0.0.0", "1.1.1.1"])
#
#

str = "139.130.4.5,    ferienhauskeck.de,google.com,8.8.4.4  ,8.8.8.8,0.0.0.0, wikipedia.org ,heise.de,raspberrypi.org"
# x = x.split(",")
# y = None
# while y != x:
#     y = x
#     x = [i.replace("  "," ") for i in x]
# x = [i.strip() for i in x]

print "cleanUnicode", cleanUnicode(var = "u'\u2103'")
print "str2list", str2list(var = str, symbol = ".")
print "cleanSpaces", cleanSpaces(var = "  N o   n e  ll ll me      ")
print "cleanType", cleanType(var = "10")
print "cleanList", cleanList(string = str)
