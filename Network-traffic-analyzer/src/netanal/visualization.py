import matplotlib.pyplot as plt

def plot_protocol_distribution(stats, output_path):
    labels = list(stats.protocol_counts.keys())
    sizes = list(stats.protocol_counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Protocol Distribution")
    plt.savefig(output_path)
    plt.close()
