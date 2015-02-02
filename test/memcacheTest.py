__author__ = 'TianShuo'

import memcache


mc = memcache.Client(['127.0.0.1:11211'], debug=0)


mc.set("testKey", "hjkhkj", 60 * 5)
mc.flush_all()

print mc.get("testKey")


mc.set("testKey", "hjkhkj", 60 * 5)
mc.delete("testKey")

print mc.get("testKey")

mc.set("testKey", "hjkhkj", 60 * 5)
print mc.get("testKey")




mc.set("intA", 2, 60 * 5)
mc.set("intB", 2, 60 * 5)
print mc.get("intA")

mc.incr("intA")
print mc.get("intA")




print mc.get('int')

