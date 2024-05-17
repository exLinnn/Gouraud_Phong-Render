#version 330 core

layout (location = 0) in vec3 aPos;   // 顶点位置
layout (location = 1) in vec3 aNormal; // 顶点法向量

out vec3 FragPos;   // 传递给片段着色器的片元位置
out vec3 Normal;     // 传递给片段着色器的法向量

uniform mat4 model;  // 模型矩阵
uniform mat4 view;   // 视图矩阵
uniform mat4 projection; // 投影矩阵

void main()
{
    // 转换顶点位置到世界空间
    FragPos = vec3(model * vec4(aPos, 1.0));
    // 转换法向量到世界空间并归一化
    Normal = normalize(mat3(model) * aNormal);

    gl_Position = projection * view * vec4(FragPos, 1.0);
}