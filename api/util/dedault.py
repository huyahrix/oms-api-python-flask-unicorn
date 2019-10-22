#  @copyright 2019 © DigiNet
#  @author ahrix<infjnite@gmail.com>
#  @create 2019/10/04 10:51
#  @update 2019/10/14 10:51
import os
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from flask import request,jsonify,Response,render_template, send_from_directory
from flask_api import status
import json


class Default(Resource):
    def get(self):
        static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        return send_from_directory('d:\\Privite\\Python\\OMSv1\\api\\templates', 'index.html')