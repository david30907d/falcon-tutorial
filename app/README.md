# Dcard Topic Recommender API

## Install

`pip install -r requirements.txt`

## API

1. use tfidf + ontology:_`/tfidf`_
	  - title
	  - context
	  - example:
		```
		http -f POST 127.0.0.1:8000/tfidf title="斜槓青年李俞潔 勇奪iPhone攝影獎第二名" context="你有聽過斜槓青年這個名詞嗎？
		以下擷取自斜槓青年這本書關於這個名詞的解釋：
		「斜槓」一詞源自於英文「Slash」，這個概念出自《紐約時報》專欄作家瑪希．艾波赫的著作。她在書中提到，如今越來越多年輕人不再滿足於「單一職 業」的生活方式，而是開始藉由多重收入、多重職業來體驗更豐富的生活。這些人在自我介紹中會用「斜槓：／」來區分不同職業，於是「斜槓」便成為他們的代名詞。
		早在 1996 年，美國學者阿蒂爾和盧梭就提出了類似的概念：無邊界職涯。無邊界職涯強調以提升個人能力替代長期雇傭保證，使員工能夠藉由跨足不同的組織體現無邊界職涯，亦即，能力才是賺錢的關鍵，只要有才華、有實力，就能藉由為不同組織服務，獲取更多收入及生活上更高的彈性。這將是未來組織變革的重要趨勢，因為在知識經濟時代，人才將取代資本成為核心生產要素，一切組織與生產都將圍繞人才展開。
		我想大家應該都有看過周遭或是新聞中有提到過的斜槓青年,這次和大家分享的斜槓青年本身職業是護理師呢！（其實我不太喜歡各大新聞媒體下的標題， 什麼台灣最正護理師贏得攝影大獎......)
		Post images
		年度手機攝影比賽「iPhone攝影獎」（iPhone Photography Awards ，IPPA）公布第11屆獲獎名單，其中最令人受矚目的是勇奪人像類第二名作品《等待》，得主是來自台灣、從事護理師工作的李俞潔。李俞潔笑說，接觸攝影5年了，沒想過第一次參賽就能得名，會走上攝影這一條路，也是因為護理師工作的 關係，「工作期間常感受到生命無常，更珍惜生活上的每一個片刻。」
		Post images
		Post images
		今年iPhone攝影獎共有140多個國家參賽，其中台灣有2名女攝影師在眾多敵人中，殺出一條血路取得佳績，一位是2016年在動物類得到第一名的平片設計師吳佳芳Erica，今年她再次拍出佳作《微笑狐狸》，奪下動物類第三名。另一位台灣之光則是當護理師10年的李俞潔，首次參賽用作品《等待》殺出重圍， 奪得人像類第二名。
		👇iPhone Photography Awards官網（很多很棒的作品，大家可以點進去欣賞）
		https://www.ippawards.com/2018-winners-people/
		https://womany.net/read/article/14316"
		```
	  - result:
		```json
		{
			"list": [
				{
					"name": "攝影",
					"postCount": 0
				},
				{
					"name": "邊界",
					"postCount": 0
				},
				{
					"name": "職業",
					"postCount": 0
				}
			]
		}
		```

## Run Server

`gunicorn --reload Topic-Recommender.app`

## Built With

falcon

## Contributors

* __張泰瑋__ [david](https://github.com/david30907d)

## License

not yet