from flask import Blueprint,jsonify, request, make_response
from BLL.compare_bll import CompareBL
comp = Blueprint('comp', __name__)
compare_bL = CompareBL()


#Get All
@comp.route("/", methods=['POST'])
def get_data_from_file():
    link_to_file = request.json
    data = compare_bL.get_data(link_to_file)
    return make_response(jsonify(data),200)
   
