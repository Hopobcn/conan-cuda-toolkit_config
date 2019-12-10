#include <cuda_runtime.h>

#include <iostream>
#include <cassert>

int main(int argc, char* argv[])
{
    int version;
    cudaError_t result = cudaRuntimeGetVersion(&version);
    assert (result != 0);
    std::cout << "CUDA runtime version: " << version << "\n";

    return 0;
}