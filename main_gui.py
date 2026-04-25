import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')   # ✅ FIX: prevents matplotlib crash
import matplotlib.pyplot as plt

print("GUI Starting...")

# ---------------- ALGORITHMS ---------------- #

def fifo(pages, capacity):
    memory = []
    faults = 0
    queue = []

    for page in pages:
        if page not in memory:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
                queue.append(page)
            else:
                removed = queue.pop(0)
                memory.remove(removed)
                memory.append(page)
                queue.append(page)
    return faults


def lru(pages, capacity):
    memory = []
    faults = 0

    for i, page in enumerate(pages):
        if page not in memory:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda x: pages[:i][::-1].index(x))
                memory.remove(lru_page)
                memory.append(page)
        else:
            memory.remove(page)
            memory.append(page)

    return faults


def optimal(pages, capacity):
    memory = []
    faults = 0

    for i, page in enumerate(pages):
        if page not in memory:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                future = pages[i+1:]
                replace = None
                farthest = -1

                for m in memory:
                    if m not in future:
                        replace = m
                        break
                    else:
                        idx = future.index(m)
                        if idx > farthest:
                            farthest = idx
                            replace = m

                memory.remove(replace)
                memory.append(page)
    return faults


# ---------------- VISUALIZATION ---------------- #

def visualize(pages, capacity, algo):
    faults_list = []

    for i in range(1, len(pages)+1):
        sub = pages[:i]

        if algo == "FIFO":
            faults = fifo(sub, capacity)
        elif algo == "LRU":
            faults = lru(sub, capacity)
        else:
            faults = optimal(sub, capacity)

        faults_list.append(faults)

    plt.figure()
    plt.plot(range(1, len(pages)+1), faults_list, marker='o')
    plt.title(f"Page Fault Growth ({algo})")
    plt.xlabel("Number of Requests")
    plt.ylabel("Page Faults")
    plt.grid()
    plt.show()


# ---------------- GUI FUNCTION ---------------- #

def run_simulation():
    try:
        pages = list(map(int, entry_pages.get().split(",")))
        capacity = int(entry_frames.get())

        algo = algo_var.get()

        if algo == "FIFO":
            faults = fifo(pages, capacity)
        elif algo == "LRU":
            faults = lru(pages, capacity)
        else:
            faults = optimal(pages, capacity)

        hits = len(pages) - faults

        result_text.set(f"""
Algorithm: {algo}
Total Pages: {len(pages)}
Page Faults: {faults}
Page Hits: {hits}
Hit Ratio: {hits/len(pages):.2f}
        """)

        visualize(pages, capacity, algo)

    except Exception as e:
        result_text.set(f"Error: {str(e)}")


# ---------------- MAIN APP ---------------- #

def main():
    global entry_pages, entry_frames, algo_var, result_text

    root = tk.Tk()
    root.title("Virtual Memory Optimization Simulator")
    root.geometry("900x500")
    root.configure(bg="#eef2f3")

    # LEFT PANEL
    frame_left = tk.Frame(root, bg="#d9e6f2", padx=10, pady=10)
    frame_left.pack(side="left", fill="y")

    tk.Label(frame_left, text="Input Configuration", font=("Arial", 12, "bold"), bg="#d9e6f2").pack(anchor="w")

    tk.Label(frame_left, text="Page Requests (comma separated):", bg="#d9e6f2").pack(anchor="w")
    entry_pages = tk.Entry(frame_left, width=30)
    entry_pages.insert(0, "7,0,1,2,0,3,0,4")
    entry_pages.pack()

    tk.Label(frame_left, text="Number of Frames:", bg="#d9e6f2").pack(anchor="w")
    entry_frames = tk.Entry(frame_left)
    entry_frames.insert(0, "3")
    entry_frames.pack()

    tk.Label(frame_left, text="Algorithm:", bg="#d9e6f2").pack(anchor="w")

    algo_var = tk.StringVar(value="FIFO")

    for algo in ["FIFO", "LRU", "Optimal"]:
        tk.Radiobutton(frame_left, text=algo, variable=algo_var, value=algo, bg="#d9e6f2").pack(anchor="w")

    tk.Button(frame_left, text="Run Simulation", command=run_simulation, bg="#4CAF50", fg="white").pack(pady=10)

    # RIGHT PANEL
    frame_right = tk.Frame(root, bg="white", padx=10, pady=10)
    frame_right.pack(side="right", expand=True, fill="both")

    tk.Label(frame_right, text="Performance Metrics", font=("Arial", 12, "bold")).pack(anchor="w")

    result_text = tk.StringVar()
    tk.Label(frame_right, textvariable=result_text, justify="left", bg="white", font=("Courier", 10)).pack(anchor="w")

    root.mainloop()


# ✅ IMPORTANT ENTRY POINT
if __name__ == "__main__":
    main()