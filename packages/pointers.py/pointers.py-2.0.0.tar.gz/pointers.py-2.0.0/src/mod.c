#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define GETOBJ PyObject* obj; if (!PyArg_ParseTuple(args, "O", &obj)) return NULL

static PyObject* add_ref(PyObject* self, PyObject* args) {
    GETOBJ;
    Py_INCREF(obj);
    Py_RETURN_NONE;
}

static PyObject* remove_ref(PyObject* self, PyObject* args) {
    GETOBJ;
    Py_DECREF(obj);
    Py_RETURN_NONE;
}

static PyObject* force_set_attr(PyObject* self, PyObject* args) {
    PyTypeObject* type;
    PyObject* value;
    char* key;

    if (!PyArg_ParseTuple(args, "OsO", &type, &key, &value)) return NULL;

    PyDict_SetItemString(type->tp_dict, key, value);
    PyType_Modified(type);

    Py_RETURN_NONE;
}



static PyMethodDef methods[] = {
    {"add_ref", add_ref, METH_VARARGS, "Increment the reference count on the target object."},
    {"remove_ref", remove_ref, METH_VARARGS, "Decrement the reference count on the target object."},
    {"force_set_attr", force_set_attr, METH_VARARGS, "Force setting an attribute on the target type."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_pointers",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit__pointers(void) {
    return PyModule_Create(&module);
}
