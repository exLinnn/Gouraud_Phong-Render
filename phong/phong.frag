#version 330 core

in vec3 FragPos;    // 从顶点着色器传递的片元位置
in vec3 Normal;      // 从顶点着色器传递的法向量

out vec4 FragColor;  // 最终的片元颜色

uniform vec3 lightPos;   // 光源位置
uniform vec3 lightColor; // 光源颜色
uniform vec3 viewPos;    // 观察者位置

void main()
{
    // 计算光源方向
    vec3 lightDir = normalize(lightPos - FragPos);
    // 计算观察方向
    vec3 viewDir = normalize(viewPos - FragPos);
    // 计算反射向量
    vec3 reflectDir = reflect(-lightDir, normalize(Normal));

    // 环境光照
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;
    
    // 漫反射光照
    float diffuseStrength = 0.5;
    vec3 diffuse = diffuseStrength * max(dot(normalize(Normal), lightDir), 0.0) * lightColor;
    
    // 镜面反射光照
    float specularStrength = 0.8;
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;
    
    // 计算最终颜色
    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}