import numpy as np
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# 着色器文件
vertex_shader_phong = "./phong/phong.vert"
fragment_shader_phong = "./phong/phong.frag"
vertex_shader_gouraud = "./gouraud/gouraud.vert"
fragment_shader_gouraud = "./gouraud/gouraud.frag"
# 当前着色器类型
current_shader_type = "phong"
# 模型文件
OBJ_PATH = "t1.obj"
#鼠标行为
mouse_down = False
last_x = 0
last_y = 0
# 相机设置
camera_position = glm.vec3(300, 140, 300)
camera_target = glm.vec3(300, 140, 0)
# 旋转速度
speed = 0.1


def mouse_callback(button, state, x, y):
    global mouse_down, last_x, last_y, current_shader_type
    if button == GLUT_LEFT_BUTTON:  # 左键控制视角旋转
        if state == GLUT_DOWN:
            mouse_down = True
            last_x, last_y = x, y
        elif state == GLUT_UP:
            mouse_down = False
    if button == GLUT_RIGHT_BUTTON:  # 右键控制着色器类型
        if state == GLUT_DOWN:
            if current_shader_type == "phong":
                current_shader_type = "gouraud"
            else:
                current_shader_type = "phong"
            print(f"Shader type switched to {current_shader_type}")
            glutSetWindowTitle(f"OBJ Renderer ({current_shader_type})")


def motion_callback(x, y):
    global last_x, last_y, view, camera_position, camera_target, speed
    if mouse_down:
        # 计算鼠标移动的偏移量
        x_offset = y - last_y
        y_offset = last_x - x

        # 根据鼠标移动构造旋转矩阵
        angle_y = glm.radians(y_offset * speed)
        angle_x = glm.radians(x_offset * speed)
        print(angle_y, angle_x)

        rotation_y = glm.rotate(glm.mat4(1.0), angle_y, glm.vec3(0, camera_target[1], 0))
        rotation_x = glm.rotate(glm.mat4(1.0), angle_x, glm.vec3(camera_target[0], 0, 0))

        camera_direction = camera_position - camera_target
        camera_direction = rotation_y * rotation_x * camera_direction

        # 确保相机方向向量仍然在球面上
        camera_direction = glm.normalize(camera_direction)
        camera_position = camera_target + 300 * camera_direction

        # 更新视图矩阵
        view = glm.lookAt(camera_position, camera_target, glm.vec3(0, 1, 0))

        last_x, last_y = x, y

class Mesh:
    def __init__(self):
        self.vert = []
        self.face = []
        self.norm = [] # 顶点法向量

# 读取并解析obj文件
def read(filename):
    with open(filename) as file:
        vert = []
        face = []
        for line in file:
            if line.startswith("#"):
                continue
            elif line.startswith("v"):
                vert.append([float(e) for e in line.split(" ")[1:]])
            elif line.startswith("f"):
                face.append([int(e)-1 for e in line.split(" ")[1:]])
    mesh = Mesh()
    mesh.vert = vert
    mesh.face = face
    return mesh

# 计算顶点法向量
def compute_vertex_normals(mesh):
    vertex_normals = np.zeros((len(mesh.vert), 3))

    for face in mesh.face:
        v1 = np.array(mesh.vert[face[0]])
        v2 = np.array(mesh.vert[face[1]])
        v3 = np.array(mesh.vert[face[2]])

        vector1 = v2 - v1
        vector2 = v3 - v1

        face_normal = np.cross(vector1, vector2)

        vertex_normals[face[0]] += face_normal
        vertex_normals[face[1]] += face_normal
        vertex_normals[face[2]] += face_normal

    vertex_normals = vertex_normals / np.linalg.norm(vertex_normals, axis=1)[:, np.newaxis]

    return vertex_normals

# 加载着色器并编译
def load_shaders():
    # 鼠标右键切换着色器类型
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    vertex_shader_src = vertex_shader_phong if current_shader_type == "phong" else vertex_shader_gouraud
    fragment_shader_src = fragment_shader_phong if current_shader_type == "phong" else fragment_shader_gouraud

    # 读取顶点着色器源代码
    with open(vertex_shader_src, 'r', encoding='utf-8') as vsh:
        vertex_code = vsh.read()
    glShaderSource(vertex_shader, vertex_code)

    # 读取片段着色器源代码
    with open(fragment_shader_src, 'r', encoding='utf-8') as fsh:
        fragment_code = fsh.read()
    glShaderSource(fragment_shader, fragment_code)
    # 编译着色器
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex_shader)
        print(error)
        return None

    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment_shader)
        print(error)
        return None

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program)
        print(error)
        return None
    glClearColor(0.5, 0.5, 0.5, 1.0)
    return program

# 初始化模型、视图、投影矩阵
def setMatrices():
    global model, view, projection, camera_position, camera_target
    model = glm.mat4(1.0)
    view = glm.lookAt(camera_position, camera_target, glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45), 800 / 600, 0.1, 1000)

# 渲染函数
def render():
    print("Starting rendering")
    global model, view, projection

    program = load_shaders()
    if program is None:
        print("Failed to load shaders")
        return

    glUseProgram(program)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    # 设置uniform变量
    glUniformMatrix4fv(glGetUniformLocation(program, b"model"), 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix4fv(glGetUniformLocation(program, b"view"), 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(glGetUniformLocation(program, b"projection"), 1, GL_FALSE, glm.value_ptr(projection))
    glUniform3f(glGetUniformLocation(program, b"lightPos"), camera_position[0], camera_position[1], camera_position[2])
    glUniform3f(glGetUniformLocation(program, b"lightColor"), 0.0, 1.0, 0.0)
    glUniform3f(glGetUniformLocation(program, b"viewPos"), camera_target[0], camera_target[1], camera_target[2])

    print("Loaded shaders")
    # 加载模型
    mesh = read(OBJ_PATH)
    if mesh is None:
        print("Failed to load OBJ file")
        return
    mesh.norm = compute_vertex_normals(mesh)
    print("Loaded OBJ file")

    # 创建并绑定VAO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # 创建并绑定VBO for vertices
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, (len(mesh.vert) * 3 * 4), np.array(mesh.vert, dtype=np.float32), GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # 创建并绑定IBO
    IBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(mesh.face) * 3 * 4, np.array(mesh.face, dtype=np.uint32), GL_STATIC_DRAW)

    # 创建并绑定EBO for normals
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, EBO)
    glBufferData(GL_ARRAY_BUFFER, (len(mesh.norm) * 3 * 4), np.array(mesh.norm, dtype=np.float32), GL_STATIC_DRAW)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # 启用深度测试
    glEnable(GL_DEPTH_TEST)

    # 绘制模型
    glDrawElements(GL_TRIANGLES, len(mesh.face) * 3, GL_UNSIGNED_INT, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    print("Rendered OBJ file")

    glutSwapBuffers()

def init():
    global window
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("OBJ Renderer (phong)")

    # 注册鼠标事件回调函数
    glutMouseFunc(mouse_callback)
    glutMotionFunc(motion_callback)

    setMatrices()


def main():
    glutDisplayFunc(render)
    glutMainLoop()

if __name__ == '__main__':
    init()
    main()
