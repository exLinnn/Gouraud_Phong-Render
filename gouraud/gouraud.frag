#version 330 core

in vec3 FragPos;    // 从顶点着色器传递的片元位置
in vec3 Normal;      // 从顶点着色器传递的法向量
in vec3 Ambient;     // 从顶点着色器传递的环境光照颜色
in vec3 Diffuse;     // 从顶点着色器传递的漫反射光照颜色
in vec3 Specular;    // 从顶点着色器传递的镜面反射光照颜色

out vec4 FragColor;  // 最终的片元颜色

void main()
{
    // 计算最终颜色
    vec3 result = Ambient + Diffuse + Specular;
    FragColor = vec4(result, 1.0);
}