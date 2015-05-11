
init:
	rm ../timevis/db/timevis.db
	touch ../timevis/db/timevis.db

post-exp:
	@echo "### POST EXP"
	@curl localhost:8000/api/v2/experiment -d @post_exp.json -X POST -s | python -m json.tool
	@echo

put-exp:
	@echo "### PUT EXP"
	@curl localhost:8000/api/v2/experiment -d @put_exp.json -X PUT -s | python -m json.tool
	@echo

get-exp:
	@echo "### GET EXP"
	@curl localhost:8000/api/v2/experiment -s | python -m json.tool
	@echo

exp: post-exp put-exp get-exp

post-layout:
	@echo "### POST LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @post_layout.json -X POST -H "Content-type: application/json" -s | python -m json.tool
	@echo

put-layout:
	@echo "### PUT LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -d @put_layout.json -X PUT -s | python -m json.tool
	@echo

get-layout:
	@echo "### GET LAYOUT"
	@curl localhost:8000/api/v2/layout?eid=1 -s | python -m json.tool
	@echo

layout: post-layout put-layout get-layout

post-plate:
	@echo "### POST PLATE"
	@curl localhost:8000/api/v2/plate?lid=1 -d @post_plate.json -X POST -H "Content-type: application/json" -s | python -m json.tool
	@echo

put-plate:
	@echo "### PUT PLATE"
	@curl localhost:8000/api/v2/plate?lid=1 -d @put_plate.json -X PUT -H "Content-type: application/json" -s | python -m json.tool
	@echo

get-plate:
	@echo "### GET PLATE"
	@curl localhost:8000/api/v2/plate?lid=1 -s | python -m json.tool
	@echo

plate: post-plate put-plate get-plate

time:
	@echo "### GET TimeSeries"
	@curl localhost:8000/api/v2/timeseries -d @post_time.json -X POST -H "Content-type: application/json" -s | python -m json.tool
	@echo

all: exp layout plate time
