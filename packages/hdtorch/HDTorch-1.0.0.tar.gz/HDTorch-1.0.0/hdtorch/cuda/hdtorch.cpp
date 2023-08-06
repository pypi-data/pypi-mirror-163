#include <torch/extension.h>

#include <c10/cuda/CUDAGuard.h>
#include <iostream>


torch::Tensor vcount_cuda(torch::Tensor inp, int width);
torch::Tensor hcount_cuda(torch::Tensor inp);
void pack_cuda(torch::Tensor inp, torch::Tensor out);
void unpack_cuda(torch::Tensor inp, torch::Tensor out);

#define CHECK_CUDA(x) TORCH_CHECK(x.is_cuda(), #x " must be a CUDA tensor")
#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
#define CHECK_INPUT(x) CHECK_CUDA(x); CHECK_CONTIGUOUS(x)

torch::Tensor vcount(torch::Tensor inp, int width) {
	CHECK_INPUT(inp)
	return vcount_cuda(inp, width);
	
}

torch::Tensor hcount(torch::Tensor inp) {
	CHECK_INPUT(inp)
	return hcount_cuda(inp);
	
}

void pack(torch::Tensor inp, torch::Tensor out) {
	CHECK_INPUT(inp)
	CHECK_INPUT(out)
	pack_cuda(inp, out);
}

void unpack(torch::Tensor inp, torch::Tensor out) {
	CHECK_CUDA(inp)
	CHECK_CUDA(out)
	unpack_cuda(inp,out);
}


PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
	m.def("vcount", &vcount, "Count HD bits vertically");
	m.def("hcount", &hcount, "Count HD bits horizontally");
	m.def("pack",   &pack,   "Pack HD bits into 32-bit integers");
	m.def("unpack", &unpack, "Unpack 32-bit integers into HD bits");
}
