from utils import *

def main():
    file_path = "graphs/soc-sign-bitcoinotc.csv"
    G = MakeGraph(file_path, input_range = (-10, 10), output_range = (0, 1))

    # Прављење фајла са хабовима
    sorted_degree = sorted(G.degree(), key = lambda x: x[1], reverse = True)
    with open('hubs.txt', '+w') as file:
        for node, degree in sorted_degree:
            file.write(f"{node},{degree}\n")

if __name__ == '__main__':
    main()