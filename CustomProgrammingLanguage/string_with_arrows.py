def string_with_arrows(ftxt, pos_start, pos_end):
    return ftxt + "\n" + " "*pos_start + "^"*(pos_end - pos_start)