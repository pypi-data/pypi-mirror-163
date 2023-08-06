#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#define MINIMP3_IMPLEMENTATION
#include "minimp3.h"

#define ALLOC_STEP 2621440


struct np3_data
{
    mp3d_sample_t *samples;
    int len;
    size_t allocated;
    int channels;
    int hz;
};
typedef struct np3_data np3_data_t;

void
np3_data_init(np3_data_t *data)
{
    data->len = 0;
    data->samples = (mp3d_sample_t*) malloc(ALLOC_STEP * sizeof(mp3d_sample_t));
    data->allocated = ALLOC_STEP;
}

void
np3_data_grow(np3_data_t *data)
{
    data->samples = (mp3d_sample_t*) realloc (
        data->samples,
        (data->allocated + ALLOC_STEP) * sizeof(mp3d_sample_t)
    );
    data->allocated += ALLOC_STEP;
}

void
np3_data_fill_info(np3_data_t *data, const mp3dec_frame_info_t *info)
{
    data->channels = info->channels;
    data->hz = info->hz;
}

void
decode_buffer(const char *buf, const size_t buf_len, np3_data_t *data)
{
    mp3dec_t mp3d;
    mp3dec_frame_info_t info;
    size_t buf_pos = 0;
    int samples;
    bool info_loaded = false;

    mp3dec_init(&mp3d);

    while(buf_pos < buf_len)
    {
        if (data->allocated - data->len < MINIMP3_MAX_SAMPLES_PER_FRAME)
        {
            np3_data_grow(data);
        }
        samples = mp3dec_decode_frame(
            &mp3d,
            (const unsigned char*)(buf + buf_pos),
            buf_len - buf_pos,
            data->samples + data->len,
            &info
        );
        samples *= info.channels;
        data->len += samples;
        buf_pos += info.frame_bytes;
        if (!info_loaded)
        {
            np3_data_fill_info(data, &info);
        }
    }
}

void
capsule_ndarray_cleanup(PyObject *capsule)
{
    void *samples = PyCapsule_GetPointer(capsule, NULL);
    free(samples);
}

static PyObject*
np3_from_bytes(PyObject *self, PyObject *args)
{
    const char *buf;
    Py_ssize_t len;
    np3_data_t data;

    if (! PyArg_ParseTuple(args, "y#:from_bytes", &buf, &len)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    np3_data_init(&data);
    decode_buffer(buf, len, &data);
    Py_END_ALLOW_THREADS

    long int dims[1];
    PyObject *ndarray;
    PyObject *capsule;

    dims[0] = data.len;
    ndarray = PyArray_SimpleNewFromData(1, dims, NPY_INT16, data.samples);
    capsule = PyCapsule_New(data.samples, NULL, capsule_ndarray_cleanup);
    if (PyArray_SetBaseObject((PyArrayObject *) ndarray, capsule) == -1) {
        return NULL;
    }

    return Py_BuildValue("Nii", ndarray, data.channels, data.hz);
}

static PyMethodDef NP3Methods[] = {
    {"from_bytes",  np3_from_bytes, METH_VARARGS,
     "Loads an mp3 from bytes object."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef nativemodule = {
    PyModuleDef_HEAD_INIT,
    "_native",
    "Almost empty module",
    -1,
    NP3Methods
};

PyMODINIT_FUNC
PyInit__native(void)
{
    import_array();
    return PyModule_Create(&nativemodule);
}
