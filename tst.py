import module.netTools as ntt

print ntt.ping_singlehost()
print ntt.ping_singlehost("0.0.0.0", 5)

#print ntt.ping_host(hosts = ["0.0.0.0", "1.1.1.1"])
