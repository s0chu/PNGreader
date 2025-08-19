def color(R , G , B , text):
    color_args = str(R) + ";" + str(G) + ";" + str(B)
    change_text_mode = "\x1b[38;2;" + color_args + "m"
    final_string = change_text_mode + str(text) + "\x1b[m" #text != string
    return final_string

