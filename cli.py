import os
from core.scanner import scan_files
from core.classifier import load_rules, classify
from core.organizer import move_file

def show_result_gui(result):
    from tkinter import Tk, Text, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH, Frame, END
    win = Tk()
    win.title("整理结果")
    frame = Frame(win)
    frame.pack(fill=BOTH, expand=True)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    text = Text(frame, yscrollcommand=scrollbar.set, width=60, height=25)
    scrollbar.config(command=text.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=BOTH, expand=True)
    if not result:
        text.insert(END, "没有需要整理的文件。")
    else:
        for category, files in result.items():
            text.insert(END, f"{category}:\n")
            for f in files:
                text.insert(END, f"    {f}\n")
            text.insert(END, "\n")
    text.config(state='disabled')
    win.mainloop()

def gui_main():
    from tkinter import Tk, Button, Label, Entry, StringVar, IntVar, Checkbutton, filedialog, Frame, LEFT

    def select_folder():
        folder = filedialog.askdirectory(title="请选择要整理的文件夹")
        folder_var.set(folder)

    def do_organize():
        directory = folder_var.get()
        if not directory or not os.path.isdir(directory):
            result_var.set("路径无效，请重新选择。")
            return
        try:
            size_threshold = int(size_var.get()) * 1024 * 1024
        except Exception:
            size_threshold = 100 * 1024 * 1024
        clean_large = clean_large_var.get() == 1
        clean_temp = clean_temp_var.get() == 1

        # 修正配置文件路径为绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rules_path = os.path.join(script_dir, "config/rules.yml")
        rules = load_rules(rules_path)
        files = []
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isfile(path):
                files.append(entry)
        result = {}
        for filename in files:
            filepath = os.path.join(directory, filename)
            category = classify(filepath, rules, size_threshold, clean_large, clean_temp)
            target_dir = os.path.join(directory, category)
            move_file(filepath, target_dir)
            result.setdefault(category, []).append(os.path.basename(filepath))
        show_result_gui(result)

    root = Tk()
    root.title("智能文件整理工具")
    root.geometry("420x260")

    Label(root, text="请选择要整理的文件夹：", font=("Arial", 12)).pack(pady=10)
    folder_var = StringVar()
    frame1 = Frame(root)
    frame1.pack()
    Entry(frame1, textvariable=folder_var, width=35).pack(side=LEFT, padx=5)
    Button(frame1, text="浏览", command=select_folder).pack(side=LEFT)

    frame2 = Frame(root)
    frame2.pack(pady=10)
    size_var = StringVar(value="100")
    Label(frame2, text="超大文件门槛(MB):").grid(row=0, column=0, sticky='w')
    Entry(frame2, textvariable=size_var, width=8).grid(row=0, column=1, padx=5)
    clean_large_var = IntVar(value=1)
    Checkbutton(frame2, text="清理超大文件", variable=clean_large_var).grid(row=1, column=0, sticky='w', pady=2)
    clean_temp_var = IntVar(value=1)
    Checkbutton(frame2, text="清理临时文件", variable=clean_temp_var).grid(row=2, column=0, sticky='w', pady=2)

    result_var = StringVar()
    Label(root, textvariable=result_var, fg="red").pack(pady=2)
    Button(root, text="开始整理", command=do_organize, width=20, height=2).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
