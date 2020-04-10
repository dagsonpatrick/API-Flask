from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)

measurement_points = [
    {
        'id': 1,
        'description': 'Ponto-01',
        'model_cam': 'Hikvision',
        'user_cam': 'admin',
        'psw_user_cam': 'ams293031',
        'ip_cam': '192.168.0.100',
        'resolution_width': '800',
        'resolution_height': '600',
        'size_contour': 100,
        'calibration_width': 7.36,
        'calibration_height': 8.36,
    },
    {
        'id': 2,
        'description': 'Ponto-02',
        'model_cam': 'Hikvision',
        'user_cam': 'admin',
        'psw_user_cam': 'ams293031',
        'ip_cam': '192.168.0.100',
        'resolution_width': '800',
        'resolution_height': '600',
        'size_contour': 100,
        'calibration_width': 7.36,
        'calibration_height': 8.36,

    }
]

#Função para adicionar autenticação nas rotas
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'admin' and auth.password == 'ams293031':
            return f(*args, **kwargs)
        return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return  decorated

#Listar todos os pontos de medição
@app.route('/measurement_points', methods=['GET'])
@auth_required
def list_points():
    return jsonify(measurement_points), 200

#Listar um ponto de medição pela descricao
@app.route('/measurement_points/<string:description>', methods=['GET'])
@auth_required
def point_per_description(description):
    #points_per_description = [point for point in measurement_points if point['description'] == description]
    for point in measurement_points:
        if point['description'] == description:
            return jsonify(point), 200
    return jsonify({'error': 'not found'}), 404

#Alterar a descrição do ponto pelo id
@app.route('/measurement_points/<int:id>', methods=['PUT'])
@auth_required
def change_description(id):
    for point in measurement_points:
        if point['id'] == id:
            point['description'] = request.get_json().get('description')
            return jsonify(point), 200
    return jsonify({'error': 'point not found'}), 404

#Listar um ponto de medição pelo id
@app.route('/measurement_points/<int:id>', methods=['GET'])
@auth_required
def points_per_id(id):
    for point in measurement_points:
        if point['id'] == id:
            return jsonify(point), 200
    return jsonify({'error': 'not found'}), 404

#Criar um ponto de medição via JSON
@app.route('/measurement_points', methods=['POST'])
@auth_required
def save_point():
    data = request.get_json()
    measurement_points.append(data)
    return jsonify(data), 201

#Remover um ponto de medição pelo id
@app.route('/measurement_points/<int:id>', methods=['DELETE'])
@auth_required
def remove_point(id):
    index = id - 1
    del measurement_points[index]

    return jsonify({'message': 'Point delete'}), 200


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)