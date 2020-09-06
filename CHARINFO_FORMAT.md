# Character info format

This one's also quite easy, as I threw it together when writing `read.py` (the first, manual, script to screenshot converter) to allow me to give myself hints on name/avatar when writing a character's dialogue.

Recommended extension: ".c.txt" or ".c.csv"

It's a CSV file. The first column is the character's name (case-insensitive, because the compiler will uppercase it to match the script), the second column is the character's nickname (case-sensitive), and the third column is the character's avatar.

```
Character One,Chara,https://vignette.wikia.nocookie.net/villains/images/c/c4/Chara_Dreemurr_%28Transparent_ver.%29/revision/latest/
Character Two,I dunno,https://discordapp.com/assets/322c936a8c8be1b803cd94861bdfa868.png
```

If you have the ability to, I would suggest hosting the character avatars on webspace you own, to avoid hammering the other servers whenever you make a meme. (In the `read.py` iteration all of the messages of one character would be done in a row (to save time creating the screenshots, but it had the side effect of reducing load on other servers), but in this iteration all of the messages are done in order.)
