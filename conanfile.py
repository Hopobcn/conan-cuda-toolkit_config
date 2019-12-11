from conans import ConanFile
from conans.tools import os_info
from conans.errors import ConanException
from pathlib import Path
import os

class CudaRuntimeConfigConan(ConanFile):
    name = "cuda-runtime_config"
    version = "10.2"
    license = "NVIDIA EULA"
    description = "NVIDIA CUDA Runtime library"
    url = "https://github.com/Hopobcn/conan-cuda-toolkit_config"
    topics = ("conan", "cuda", "cuda-runtime", "cuda-toolkit")
    build_policy = "missing"
    
    options = {"shared": [True, False]}
    default_options = {'shared': 'True'}

    def system_requirements(self):
        if not os.path.exists(self._cuda_runtime_include):
            raise ConanException("CUDA runtime include directory: {} not found", self._cuda_runtime_include)
        if not os.path.exists(self._cuda_runtime_lib):
            raise ConanException("CUDA runtime library : {} not found", self._cuda_runtime_lib)
        if not os.path.exists(self._cuda_toolkit_bin):
            raise ConanException("nvcc : {} not found", self._cuda_toolkit_bin)
    
    def package_id(self):
        self.info.header_only()
        self.info.options.cuda_version = self._cuda_version
    
    def package_info(self):
        if self.have_cuda_toolkit:
            self.cpp_info.includedirs.append(self._cuda_runtime_include)
            self.cpp_info.libs.append(self._cuda_runtime_ldname)
            #self.cpp_info.resdirs
            self.cpp_info.libdirs.append(self._cuda_runtime_lib)
            self.cpp_info.bindirs.append(self._cuda_toolkit_bin)
            # user_info here
            self.env_info.path.append(self._cuda_runtime_lib)
            self.env_info.path.append(self._cuda_toolkit_bin)

    @property
    def have_cuda_toolkit(self):
        if not os.path.exists(self._cuda_runtime_include):
            return False
        if not os.path.exists(self._cuda_runtime_lib):
            return False
        if not os.path.exists(self._cuda_toolkit_bin):
            return False
        return True

    @property
    def _dynamic_lib_sufix(self):
        return "dylib" if os_info.is_macos else "so"

    @property
    def _cuda_runtime_dynamic_ldname(self):
        return "cudart.dll" if os_info.is_windows else "libcudart.{}".format(self._dynamic_lib_sufix)

    @property
    def _cuda_runtime_static_ldname(self):
        return "cudart_static.lib" if os_info.is_windows else "libcudart_static.a"

    @property
    def _cuda_runtime_ldname(self):
        return self._cuda_runtime_dynamic_ldname if self.options.shared else self._cuda_runtime_static_ldname
    
    @property
    def _cuda_version(self):
        return self.version
    
    @property
    def _cuda_runtime_default_install_path(self):
        if os_info.is_windows:
            windows_program_files = os.getenv('ProgramFiles', "\Program Files")
            default_install_path = Path("{}/NVIDIA GPU Computing Toolkit/CUDA/v{}".format(windows_program_files, self._cuda_version))
        elif os_info.is_macos:
            default_install_path = "/Developer/NVIDIA/CUDA-{}".format(self._cuda_version)
        else:
            default_install_path = "/usr/local/cuda-{}".format(self._cuda_version)
        return default_install_path

    @property
    def _cuda_runtime_install_path(self):
        return os.getenv('CUDA_HOME', self._cuda_runtime_default_install_path)

    @property
    def _cuda_runtime_include(self):
        return os.path.join(self._cuda_runtime_install_path, "include")

    @property
    def _cuda_runtime_lib(self):
        return os.path.join(self._cuda_runtime_install_path, "lib64")
    
    @property
    def _cuda_toolkit_bin(self):
        return os.path.join(self._cuda_runtime_install_path, "bin")
