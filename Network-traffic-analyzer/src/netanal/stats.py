from collections import Counter

protocols = Counter()
sources = Counter()

def update_stats(packet):
    protocols[packet["type"]] += 1
    sources[packet["src"]] += 1
