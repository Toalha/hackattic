def caesar_shift_char(char, offset):
    """
    Shifts a single character by a given offset, wrapping around the alphabet.
    Non-alphabetic characters are returned unchanged.
    """
    if char.isalpha():  # Check if the character is a letter
        # Determine the base (ASCII value of 'a' for lowercase, 'A' for uppercase)
        base = ord('a') if char.islower() else ord('A')
        # Shift the character and wrap around using modulo 26
        shifted_char = chr((ord(char) - base + offset) % 26 + base)
        return shifted_char
    else:
        return char  # Return non-alphabetic characters unchanged

plaintext = "gpxy, mvde, sbjk! kptwkzarfp ciopcw-mjhsgmg unmqrz. mzztfpjldtndkkq! ujh xusccszz wh \"ztlmu-hzcpd\"."
offset = 0 #you have to find it :) #this value was reverse engineered by analyzing the last sentence which looked something like "the (...?) is ..." and then finding patterns in the letters
solved_ans = ""

for char in plaintext:
    solved_ans = solved_ans + caesar_shift_char(char, offset)
    offset-=1

#The actual solution starts with capital letters
print(solved_ans)
