from Util import float_to_bin, merge_files

print(float_to_bin(8))

merge_files(["Operators/Bitwise.ipynb",
             "Operators/Bitwise And.ipynb",
             "Operators/Bitwise Or.ipynb",
             "Operators/Bitwise Not.ipynb",
             "Operators/Bitwise Xor.ipynb",
             "Operators/Bitwise Left Shift.ipynb",
             "Operators/Bitwise Right Shift.ipynb"], "dest.ipynb")
