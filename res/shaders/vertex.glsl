#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec4 colour;

uniform mat4 proj_mat;

smooth out vec4 vertex_colour;

void main() {
	vec4 actual_pos = vec4(pos, 1.0);
	gl_Position = actual_pos * proj_mat;
	vertex_colour = colour;
}