import os
import subprocess

from flask import Flask, request, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__, static_folder='./inference')
CORS(app)

os.makedirs('./inference/output', exist_ok=True)
os.makedirs('./inference/input', exist_ok=True)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('./inference/input', filename)
    file.save(file_path)

    # 根据文件扩展名判断是图像还是视频
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        process_command = ['python', 'detect.py', '--source', file_path, '--weights', './weights/best.pt']
    elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
        process_command = ['python', 'detect.py', '--source', file_path, '--weights', './weights/best.pt']
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # 调用detect.py脚本进行检测
    result = subprocess.run(
        process_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        # 获取标准输出
        output_message = result.stdout.decode('utf-8')
        # 获取错误输出
        full_message = f"STDOUT:\n{output_message}\n"
    else:
        error_message = result.stderr.decode('utf-8')
        print(f"Error in detection: {error_message}")
        return f"Error in detection: {error_message}", 500

    # 假设detect.py脚本将输出保存到了'output'文件夹
    output_image_path = os.path.join('./inference/output', filename)

    # 确保检测结果的文件存在
    if not os.path.isfile(output_image_path):
        return jsonify({"error": "Detection did not produce an output file"}), 500

    # 生成输出图像的URL
    image_url = url_for('static', filename=f'input/{filename}', _external=True)
    draw_url = url_for('static', filename=f'output/{filename}', _external=True)
    # 返回包含图像URL的JSON对象
    return jsonify({
        "image_url": image_url,
        "draw_url": draw_url,
        "image_info": full_message,  # 添加此行以返回执行信息
        "additional_info": "some_other_information"
    })


@app.route('/up', methods=['POST', 'GET'])
def upload_area():
    # start_time = time.time()
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('./inference/input', filename)
    file.save(file_path)

    # 根据文件扩展名判断是图像还是视频
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        process_command = ['python', 'area_detect.py', '--source', file_path, '--weights', './weights/best.pt']
    elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
        process_command = ['python', 'area_detect.py', '--source', file_path, '--weights', './weights/best.pt']
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # 调用detect.py脚本进行检测
    result = subprocess.run(
        process_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        # 获取标准输出
        output_message = result.stdout.decode('utf-8')
        # 获取错误输出
        full_message = f"STDOUT:\n{output_message}\n"
    else:
        error_message = result.stderr.decode('utf-8')
        print(f"Error in detection: {error_message}")
        return f"Error in detection: {error_message}", 500

    # 假设detect.py脚本将输出保存到了'output'文件夹
    output_image_path = os.path.join('./inference/output', filename)

    # 确保检测结果的文件存在
    if not os.path.isfile(output_image_path):
        return jsonify({"error": "Detection did not produce an output file"}), 500

    # 生成输出图像的URL
    image_url = url_for('static', filename=f'input/{filename}', _external=True)
    draw_url = url_for('static', filename=f'output/{filename}', _external=True)
    # end_time = time.time()
    # duration = end_time - start_time
    # 返回包含图像URL的JSON对象
    return jsonify({
        "image_url": image_url,
        "draw_url": draw_url,
        "image_info": full_message,  # 添加此行以返回执行信息
        "additional_info": "some_other_information",
        # "processing_time": duration
    })


if __name__ == '__main__':
    app.run(debug=True)
