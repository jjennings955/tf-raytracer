TF_CFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_compile_flags()))') )
TF_LFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_link_flags()))') )
bvh:
    nvcc -std=c++11 -c -o morton.cu.o morton.cu.cc ${TF_CFLAGS[@]} -D GOOGLE_CUDA=1 -x cu -Xcompiler -fPIC
    g++ -std=c++11 -shared morton.cc morton.cu.o -o morton.so -fPIC ${TF_CFLAGS[@]} ${TF_LFLAGS[@]} -O2