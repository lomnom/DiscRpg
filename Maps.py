from Tiles import *

levels=[
	RpgMap( #level 0
		[
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [path]*4 + [pathedge] + [void]*3,
			[void]*4 + [portal("stcrage",1,4,9),path,path,food] + [pathedge] + [void]*3
		],
		errMov # when moved out of bounds
	),
	RpgMap( #level 1
		[
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [portal("walkw y",0,4,13)] + [path]*13 + [oldMan] + [pathedge] + [void]*3,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19
		],
		errMov # when moved out of bounds
	),
	RpgMap( #level 1 with portal
		[
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [portal("exi+",3,4,13)] + [path]*14 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*15 + [pathedge] + [void]*3,
			[void]*4 + [path]*14 + [oldMan] + [pathedge] + [void]*3,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19,
			[void]*4 + [void]*19
		],
		errMov # when moved out of bounds
	),
	RpgMap( #exit
		[
			[void]*4 + [portal("stcrage",2,5,3)] + [path]*6 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [path]*7 + [pathedge] + [void]*3,
			[void]*4 + [portal("main rcad",3,0,0)] + [path]*6 + [pathedge] + [void]*3
		],
		errMov # when moved out of bounds
	)
]

spawns=[
	[4,0],
	[5,3]
]