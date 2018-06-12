# coding=utf-8
from flask import Blueprint, render_template, request
import json
from models import TimelineStore, TItem
from datetime import datetime
import pdb

bp = Blueprint('api_timelines', __name__, url_prefix='/api/timelines')

@bp.route('/', methods=['GET'])
def timeline_index():
    ts = TimelineStore()
    rs = ts.getAllTItem().getList()
    ts.close()
    if not rs:
        return "empty" ,400
    rs = map(vars,rs)
    return json.dumps(rs, default=str)

@bp.route('/<id>', methods=['GET'])
def timeline_by_id(id):
    ts = TimelineStore()
    rs = ts.getAllTItem().getList()
    ts.close()
    if not rs:
        return "empty" ,400
    rs = map(vars,rs)
    return json.dumps(rs, default=str)

bp2 = Blueprint('api_titems', __name__, url_prefix='/api/titems')

@bp2.route('/', methods=['GET','POST'])
def titems():
    if request.method == 'GET':
        ts = TimelineStore()
        rs = ts.getAllTItem().getList()
        ts.close()
        if not rs:
            return "empty" ,400
        rs = map(vars,rs)
        return json.dumps(rs, default=str)
    elif request.method == 'POST':
        ts = TimelineStore()
        try:
            # pdb.set_trace()
            print "r: " + request.data
            json_dict = request.get_json(silent=True)
            print json_dict
        except:
            return "error", 422
        json_dict["timestamp"] = datetime.fromtimestamp(int(json_dict["timestamp"])/1000) # only because time in js is in milliseconds
        tItem = TItem(**json_dict)  
        tItem, created = ts.saveTItem(tItem)
        ts.close()
        if created:
            # pdb.set_trace()
            return json.dumps(vars(tItem), default=str), 201
        else:
            # print tItem
            return 'duplicate', 400

@bp2.route('/<id>', methods=['GET','DELETE'])
def titem(id):
    timestamp, title = id.split("_")
    timestamp= datetime.fromtimestamp(int(timestamp)/1000) # only because time in js is in milliseconds
    tItem = TItem(timestamp, title) 
    ts = TimelineStore()
    if request.method == 'GET':
        try:
            tItem = ts.getTItem(tItem)
            # pdb.set_trace()
            return json.dumps(vars(tItem), default=str)
        except:
            return "not exist",404
    elif request.method == 'DELETE':
        if ts.deleteTItem(tItem):
            ts.close()
            return "deleted", 204
