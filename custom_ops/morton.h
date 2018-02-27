// kernel_example.h
#ifndef BVH_H
#define BVH_H

template <typename Device, typename T>
struct MortonFunctor {
  void operator()(const Device& d, int size, const T* in, T* out);
};

#if GOOGLE_CUDA
// Partially specialize functor for GpuDevice.
template <typename Eigen::GpuDevice, typename T>
struct MortonFunctor {
  void operator()(const Eigen::GpuDevice& d, int size, const T* in, T* out);
};
#endif

#endif BVH_H