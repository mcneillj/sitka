#define PY_SSIZE_T_CLEAN
#include <Python.h>
//#include <Windows.h>
#include <cmath>

const double e = 2.7182818284590452353602874713527;
const double PI = 3.141592653589793238462643383279;

PyObject* calculate_equation_of_time_impl(PyObject*, PyObject* o) {
	double gamma = PyFloat_AsDouble(o);
	double cosgamma = cos((gamma) * PI / 180);
	double singamma = sin(gamma * PI / 180);
	double cos2gamma = cos((2 * gamma) * PI / 180);
	double sin2gamma = sin((2 * gamma) * PI / 180);
	double equation_of_time = 2.2918 * (0.0075 + 0.1868 * cosgamma - 3.2077 * singamma - 1.4615 * cos2gamma - 4.089 * sin2gamma);
	return PyFloat_FromDouble(equation_of_time);
}

static PyMethodDef solar_methods[] = {
	// The first property is the name exposed to Python, fast_tanh, the second is the C++
	// function name that contains the implementation.
	{ "calculate_equation_of_time", (PyCFunction)calculate_equation_of_time_impl, METH_O, nullptr },

	// Terminate the array with an object containing nulls.
{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef solar2_module = {
	PyModuleDef_HEAD_INIT,
	"solar2",                        // Module name to use with Python import statements
	"Provides some functions, but faster",  // Module description
	0,
	solar_methods                   // Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_solar2() {
	return PyModule_Create(&solar2_module);
}