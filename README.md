# README

本项目实现了 gouraud、phong 两种着色器，并加载 .obj 文件进行 OpenGL 渲染。

## 模块功能

代码当中，实现了 OpenGL 渲染所必须的几个模块如下：

-   `init()`：初始化模块。代码采用 OpenGL 原生的`GLUT`窗口展示渲染的模型，初始化窗口并绑定鼠标回调函数。
-   `load_shaders()`：将着色器加载、编译、链接，保存在 OpenGL 项目变量`program`中返回。
-   `render()`：渲染函数，实现了 OpenGL 渲染。具体步骤大致如下：
    -   获取着色器 program，设置着色器的外部变量，包括投影矩阵、视图矩阵，相机设置、光源设置等；
    -   加载.obj 文件获取模型，计算顶点法向量；
    -   创建 VAO、VBO（顶点）、IBO（索引）、EBO（法向量）等指针，根据 obj 模型设置好参数，并绑定在 OpenGL 项目上；
    -   启动深度测试，绘制模型。
-   `mouse_callback(button, state, x, y) / motion_callback(x, y)`：涉及鼠标行为的两个回调函数。`mouse_callback`函数会检测鼠标行为，主要负责点击行为。当点击右键时负责切换着色器类型。`motion_callback`主要负责拖动行为，更新旋转视图矩阵并返回。

## 使用说明

确保运行环境满足要求后可直接运行，运行成功，弹出 OpenGL 渲染窗口。

-   按住鼠标左键拖动，可以实现视角拖动。
-   单击鼠标右键，可以实现两种着色器的切换。窗口名称中，会提示当前使用的是哪一种着色器。
-   代码当中的全局变量，用户可以进行更改，大致包括：
    -   着色器文件路径；
    -   模型文件路径；
    -   模型的中心点（相机的瞄准点）；
    -   视角的旋转速度。
