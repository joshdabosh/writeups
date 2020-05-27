# Is-This-Crypto?
Crypto, 50

Very epic challenge.

We are given `Òãèáåþöãðáùè±øâ±ð±õøâòøáýøÿô±åùðå±ùðâ±óôôÿ±ðãþäÿõ±÷þã±àäøåô±ð±ýþÿö±åøüô½±óäå±øÿ±ãôòôÿå±åøüôâ±øå±ùðâ±âôôÿ±ðÿ±ôéáýþâøþÿ±þ÷±ãôâôðãòù±ðÿõ±øüáýôüôÿåðåøþÿ¿±Åùøâ±õøâòøáýøÿô±âôôúâ±åþ±áãþçøõô±âôòäãô±òþüüäÿøòðåøþÿ±ðÿõ±âùðãôõ±õðåð±âåþãðöô±äâøÿö±áäóýøò±úôè±òãèáåþöãðáùè½±æùøòù±ôââôÿåøðýýè±ãôõäòôâ±åùô±õðüðöô±åùðå±òðÿ±óô±õþÿô±åùãþäöù±ôÿòãèáåøþÿ¿››åûòå÷êÿ¡Îåù ¤ÎøâÎúèý¢ì››Åùô±Õðåð±Òôÿåãô±Âåðÿõðãõ±÷þã±Òþÿ÷øõôÿåøðýøåè±ðÿõ±Øÿåôöãøåè±âåðåôâ±åùðå±ð±òþüáäåôã±âèâåôü±üäâå±ÿþå±òþÿåðøÿ±ðÿè±øÿ÷þãüðåøþÿ±åùðå±òðÿÿþå±óô±áãþçøõôõ±ðå±åùô±åøüô±þ÷±ãôàäôâåøÿö±øå¿±Åùô±áäãáþâô±þ÷±åùøâ±âåðÿõðãõ±øâ±åþ±ôÿâäãô±åùðå±ÿþ±õðåð±÷ãþü±ð±òþÿÿôòåôõ±òþüáäåôã±âèâåôü±òðÿ±óô±ðòòôââôõ±óè±ðÿ±äÿðäåùþãøâôõ±áðãåè¿±Åùøâ±æþäýõ±ðýýþæ±äâôãâ±åþ±áãþåôòå±åùôøã±õðåð±ðÿõ±üðúô±åùôøã±áôãâþÿðý±øÿ÷þãüðåøþÿ±âôòäãô½±æùøòù±øâ±üþãô±øüáþãåðÿå±åùðÿ±ôçôã¿` as a ciphertext and we are told to go and decrypt it.

My solution was:
Take ordinal of first character (`Ò`, 220). Subtract 65 (`A`) from 220. Brute force a bit for offset, and subtract that from every character's ordinal value.

This gets us to some suspicious looking text, which is semi legible, when we try subtract 143:
`CTYRVogTaRjY"iS"a"fiSciRnipe"VjaV"...` and so on.

Suspicious. The first word is almost definitely `Cryptography`. So we try to xor "C" (67) with "Ò" (220). We get 145.

We xor everything else with 145, and get the flag.
`Cryptography is a discipline that has been around for quite a long time, but in recent times it has seen an explosion of research and implementation. This discipline seeks to provide secure communication and shared data storage using public key cryptography, which essentially reduces the damage that can be done through encryption.₫₫tjctf{n0_th 5_is_kyl3}₫₫The Data Centre Standard for Confidentiality and Integrity states that a computer system must not contain any information that cannot be provided at the time of requesting it. The purpose of this standard is to ensure that no data from a connected computer system can be accessed by an unauthorised party. This would allow users to protect their data and make their personal information secure, which is more important than ever.`

Flag: `tjctf{n0_th15_is_kyl3}`

If there was a missing character it was because copy pasting the unicode is bad, but you could just guess the missing character.
