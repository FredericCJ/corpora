# audio-rt-ground — config/toolchain-linux-clang.cmake
# Linux leg: clang/LLVM + lld, same major as the Windows leg (booklet section 10.1: one family,
# two legs; the hub pins the floor version per release — reference/audio_platform_baseline_manifest.md
# H4). Law: reference/toolchain_build_manifest.md B2/B4/B9.
# This file was authored on the Windows reference machine and is NOT battery-verified on a Linux
# host [CC-FACT verify-before-use: run one dev configure+build on the Linux leg, then move this
# comment to a hub row].

# NOTE (CMake mechanics, CC-FACT): setting CMAKE_SYSTEM_NAME flips CMAKE_CROSSCOMPILING to TRUE
# even for a native build. Do not key logic off CMAKE_CROSSCOMPILING in this repo.
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

# Deployment pins an absolute versioned path (e.g. /usr/bin/clang-<major>, or the upstream
# toolchain's prefix) — hub H4 owns the pin. "clang" from PATH is the skeleton default only.
set(CMAKE_C_COMPILER   "clang")
set(CMAKE_CXX_COMPILER "clang++")

# Configure-time triple assertion, the Linux analog of the Windows leg's UCRT/triple row.
# Distro triples legitimately vary in the vendor field (x86_64-pc-linux-gnu,
# x86_64-unknown-linux-gnu, ...) [CC-FACT], so match the invariant parts only.
execute_process(
  COMMAND "${CMAKE_C_COMPILER}" -print-target-triple
  OUTPUT_VARIABLE _audio_triple
  OUTPUT_STRIP_TRAILING_WHITESPACE
  RESULT_VARIABLE _audio_triple_rc)
if(NOT _audio_triple_rc EQUAL 0 OR NOT _audio_triple MATCHES "^x86_64-[A-Za-z0-9_]+-linux-gnu$")
  message(FATAL_ERROR
    "audio-rt-ground: compiler target triple is '${_audio_triple}', expected "
    "x86_64-<vendor>-linux-gnu. Wrong compiler on PATH; see "
    "reference/toolchain_build_manifest.md B4/B11 and hub H4.")
endif()

# --- linker: lld on both legs (booklet section 10.4) ------------------------------------------
set(CMAKE_EXE_LINKER_FLAGS_INIT    "-fuse-ld=lld")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "-fuse-ld=lld")
set(CMAKE_MODULE_LINKER_FLAGS_INIT "-fuse-ld=lld")

# Per-leg flag rows (-fno-plt; -Wl,-z,relro -Wl,-z,now) live in CMakePresets.json as
# AUDIO_FLAGS_LEG / AUDIO_LDFLAGS_LEG on the linux-* presets — documented rows in the canon
# (toolchain_build_manifest.md B2/B4), never ad hoc, never in this file.
