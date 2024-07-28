from flask import Flask, request, jsonify
from flask_cors import CORS  # 引入 CORS
import main

app = Flask(__name__)
CORS(app)  # 应用 CORS 到您的 Flask 应用


@app.route('/api/vm', methods=['POST'])
def vm():
    # 获取前端传递的虚拟机信息
    data = request.get_json()
    operation = data["operation"]

    # 在这里执行KVM管理操作，创建虚拟机
    data = main.operation_bus(operation, data)
    return jsonify(data)


@app.route('/api/getInfo', methods=['GET'])
def get_info():
    # 在这里执行KVM管理操作
    data = main.get_all_vm_info()

    return jsonify(data)


@app.route('/api/hostInfo', methods=['GET'])
def get_host_info():
    # 在这里执行KVM管理操作
    data = main.get_host_info()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
