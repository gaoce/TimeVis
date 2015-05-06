
init:
	rm ../timevis/db/timevis.db
	touch ../timevis/db/timevis.db

get-exp:
	@echo "### GET EXP"
	@curl localhost:8000/api/v2/experiment
	@echo

post-exp:
	@echo "### POST EXP"
	@curl localhost:8000/api/v2/experiment -d @exp_new.json -X POST
	@echo

put-exp:
	@echo "### PUT EXP"
	@curl localhost:8000/api/v2/experiment -d @exp_changed.json -X PUT
	@echo

exp: post-exp put-exp get-exp

get-layout:
	@echo "### GET LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1
	@echo

post-layout:
	@echo "### POST LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @layout_new.json -X POST -H "Content-type: application/json"
	@echo

put-layout:
	@echo "### PUT LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @layout_changed.json -X PUT
	@echo

layout: post-layout put-layout get-layout

all: exp layout
