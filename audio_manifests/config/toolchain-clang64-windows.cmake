# audio-rt-ground — config/toolchain-clang64-windows.cmake
# Windows leg: MSYS2 CLANG64, clang/LLVM + lld, UCRT. Law: reference/toolchain_build_manifest.md
# B2/B4/B9; versions are hub rows (reference/audio_platform_baseline_manifest.md H2/H3).
# Pinned triple: x86_64-w64-windows-gnu (UCRT). [MEASURED 2026-08-12: clang 22.1.8,
#   `clang -print-target-triple` -> x86_64-w64-windows-gnu]
# The build refuses foreign environments (booklet section 10.1): mixed-runtime binaries are the
# MSYS2 ecosystem's classic self-inflicted wound. Two guards below: MSYSTEM shell check and a
# configure-time triple assertion. Both are build-catchable rows.

# --- guard 1: must run inside a CLANG64 shell (MSYSTEM=CLANG64) -------------------------------
# Escape hatch AUDIO_ALLOW_FOREIGN_SHELL is diagnostic-only; shipping through it is a defect.
if(NOT "$ENV{MSYSTEM}" STREQUAL "CLANG64" AND NOT AUDIO_ALLOW_FOREIGN_SHELL)
  message(FATAL_ERROR
    "audio-rt-ground: Windows leg builds ONLY from a CLANG64 shell "
    "(MSYSTEM='$ENV{MSYSTEM}'). Launch C:/msys64/clang64.exe, or pass "
    "-DAUDIO_ALLOW_FOREIGN_SHELL=ON for diagnosis only. "
    "See reference/toolchain_build_manifest.md B4.")
endif()

# NOTE (CMake mechanics, CC-FACT): setting CMAKE_SYSTEM_NAME in a toolchain file flips
# CMAKE_CROSSCOMPILING to TRUE even when host == target. Harmless for this native build; do not
# key logic off CMAKE_CROSSCOMPILING in this repo.
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR AMD64)

# Absolute paths: PATH pollution from other MSYS2 subsystems must not be able to redirect the
# compiler. clang++ is present only for vendored C++ dependencies; the product is C17.
set(CMAKE_C_COMPILER   "C:/msys64/clang64/bin/clang.exe")
set(CMAKE_CXX_COMPILER "C:/msys64/clang64/bin/clang++.exe")

# --- guard 2: configure-time triple assertion (the UCRT/triple row, booklet section 10.1) -----
execute_process(
  COMMAND "${CMAKE_C_COMPILER}" -print-target-triple
  OUTPUT_VARIABLE _audio_triple
  OUTPUT_STRIP_TRAILING_WHITESPACE
  RESULT_VARIABLE _audio_triple_rc)
if(NOT _audio_triple_rc EQUAL 0 OR NOT _audio_triple STREQUAL "x86_64-w64-windows-gnu")
  message(FATAL_ERROR
    "audio-rt-ground: compiler target triple is '${_audio_triple}', expected "
    "'x86_64-w64-windows-gnu' (CLANG64/UCRT). Wrong toolchain on PATH or wrong package set; "
    "see reference/toolchain_build_manifest.md B4/B11 and hub H3.")
endif()

# --- linker: lld on both legs (booklet section 10.4) ------------------------------------------
# lld is CLANG64's default linker; forcing it keeps the pin explicit and survives environment
# drift. [MEASURED 2026-08-12: -fuse-ld=lld links and runs; lld MinGW driver handles
# -Wl,-Map=, -Wl,--gc-sections, -Wl,--thinlto-cache-dir=, -Wl,--wrap=malloc]
set(CMAKE_EXE_LINKER_FLAGS_INIT    "-fuse-ld=lld")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "-fuse-ld=lld")
set(CMAKE_MODULE_LINKER_FLAGS_INIT "-fuse-ld=lld")

# Flag law lives in CMakePresets.json cache variables (AUDIO_FLAGS_*) consumed by CMakeLists —
# never here, never per-file (canon rule, toolchain_build_manifest.md B1/B2).
