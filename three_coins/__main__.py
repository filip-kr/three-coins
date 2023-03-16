from db import conn
from gui import root, ttk
from helper.hex import ProtoHexagram
from helper.counter import Counter


def main():
    proto_hex = ProtoHexagram()
    counter = Counter()

    def __get_hex_line():
        if counter.count < 6:
            proto_hex.add_line(counter.count)
            print(proto_hex.lines[counter.count])
            counter.add(1)
        else:
            true_hex = conn.get_by_binary(proto_hex.binary)
            print(true_hex, proto_hex.lines)

            if 6 not in proto_hex.lines and 9 not in proto_hex.lines:
                exit('No changing lines')

            reverse_hex = conn.get_by_binary(proto_hex.reverse_binary)
            print(reverse_hex)

    qstn_label = ttk.Label(root, text='What is your question?')
    qstn_label.pack()

    qstn_txtbox = ttk.Entry(root, textvariable=qstn_label)
    qstn_txtbox.pack()
    qstn_txtbox.focus()

    ttk.Button(root, text='Toss coins', command=__get_hex_line).pack()
    root.mainloop()
