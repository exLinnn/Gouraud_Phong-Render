#version 330 core

layout (location = 0) in vec3 aPos;  // 顶点位置
layout (location = 1) in vec3 aNormal; // 顶点法向量

out vec3 FragPos;   // 传递给片段着色器的片元位置
out vec3 Normal;     // 传递给片段着色器的法向量
out vec3 Ambient;    // 传递环境光照的颜色
out vec3 Diffuse;    // 传递漫反射光照的颜色
out vec3 Specular;   // 传递镜面反射光照的颜色

uniform mat4 model;  // 模型矩阵
uniform mat4 view;   // 视图矩阵
uniform mat4 projection; // 投影矩阵
uniform vec3 lightPos;   // 光源位置
uniform vec3 lightColor; // 光源颜色
uniform vec3 viewPos;    // 观察者位置

void main()
{
    // 转换顶点位置到世界空间
    FragPos = vec3(model * vec4(aPos, 1.0));
    // 转换法向量到世界空间并归一化
    Normal = normalize(mat3(model) * aNormal);

    // 计算光源方向
    vec3 lightDir = normalize(lightPos - FragPos);
    // 计算观察方向
    vec3 viewDir = normalize(viewPos - FragPos);
    // 计算反射向量
    vec3 reflectDir = reflect(-lightDir, normalize(Normal));

    // 环境光照
    float ambientStrength = 0.2;
    Ambient = ambientStrength * lightColor;
    
    // 漫反射光照
    float diffuseStrength = 0.5;
    Diffuse = diffuseStrength * max(dot(normalize(Normal), lightDir), 0.0) * lightColor;
    
    // 镜面反射光照
    float specularStrength = 0.8;
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    Specular = specularStrength * spec * lightColor;
    
    gl_Position = projection * view * vec4(FragPos, 1.0);
}