
init:
	rm ../timevis/db/timevis.db
	touch ../timevis/db/timevis.db

get-exp:
	curl localhost:8000/api/v2/experiment
	@echo

post-exp:
	curl localhost:8000/api/v2/experiment -d @exp_new.json -X POST
	@echo

put-exp:
	curl localhost:8000/api/v2/experiment -d @exp_changed.json -X PUT
	@echo

exp: post-exp put-exp get-exp

get-layout:
	curl localhost:8000/api/v2/layout?eid=1
	@echo

post-layout:
	curl localhost:8000/api/v2/layout?eid=1 -d @layout_new.json -X POST -H "Content-type: application/json"
	@echo

put-layout:
	curl localhost:8000/api/v2/layout?eid=1 -d @layout_changed.json -X PUT
	@echo

layout: post-layout put-layout get-layout
