
init:
	rm ../timevis/db/timevis.db
	touch ../timevis/db/timevis.db

get-exp:
	@echo "### GET EXP"
	@curl localhost:8000/api/v2/experiment -s | python -m json.tool
	@echo

post-exp:
	@echo "### POST EXP"
	@curl localhost:8000/api/v2/experiment -d @exp_new.json -X POST -s | python -m json.tool 
	@echo

put-exp:
	@echo "### PUT EXP"
	@curl localhost:8000/api/v2/experiment -d @exp_changed.json -X PUT -s | python -m json.tool 
	@echo

exp: post-exp put-exp get-exp

get-layout:
	@echo "### GET LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -s | python -m json.tool 
	@echo

post-layout:
	@echo "### POST LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @layout_new.json -X POST -H "Content-type: application/json" -s | python -m json.tool 
	@echo

put-layout:
	@echo "### PUT LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @layout_changed.json -X PUT -s | python -m json.tool 
	@echo

layout: post-layout put-layout get-layout

all: exp layout
