# Sarah-Palin-Fanpage
Web, 35

>  Written by jpes707
>  Are you a true fan of Alaska's most famous governor? Visit the Sarah Palin fanpage.
 
The [exclusive fanpage](https://sarah_palin_fanpage.tjctf.org/exclusive
) requires liking all 10 of Sarah Palin's top 10 moments. The `data` cookie seems to be a base64 encoded JSON string:

```json
{"1":false,"2":false,"3":false,"4":false,"5":false,"6":false,"7":false,"8":false,"9":false,"10":false}
```

We can guess that these numbers refer to Sarah Palin's top 10 moments. Changing them all to true gives us the flag, base64 encoding, and setting the cookie gives us the flag.

Flag: `tjctf{wkDd2Pi4rxiRaM5lOcLo979rru8MFqVHKdTqPBm4k3iQd8n0sWbBkOfuq9vDTGN9suZgYlH3jq6QTp3tG3EYapzsTHL7ycqRTP5Qf6rQSB33DcQaaqwQhpbuqPBm4k3iQd8n0sWbBkOf}`