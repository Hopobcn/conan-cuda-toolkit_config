# conan-cuda-toolkit_config

A conan best-effort *virtual* package for NVIDIA CUDA runtime.
This package is not a normal conan package in the sense that it doesn't package anything.

This package searches the location of the CUDA runtime installation and populates the `cpp_info` accordingly.
To work well, this package has to be regenerated in every consumer machine.
If those consumers don't have a CUDA installation, this package with do nothing more than fail.
