# -*- coding: utf-8 -*-
# PHASE 1 fact records — corpus: emb-ops (Operational Use of C and C++ in Embedded Contexts)
# Source report: compass_artifact_wf-4687a3e1-... Raw tags: tier (trunk|c-leaf|cpp-leaf) | theme | type | verification.
# NOTE: the report lists the GCC manual three times (manual, Optimize Options chapter, -fstack-usage);
# those are one work — recorded once with all three themes, merge logged in corpus_report.md.
R = []
C = 'emb-ops'
def n(id, title, au, yr, typ, tier, theme, ver='verified', note='', ident='', key=''):
    R.append(dict(id=id, corpus=C, title=title, authors=au, year=yr, rtype=typ,
                  verification=ver, note=note, ident=ident, unresolved=[],
                  raw=dict(tier=tier, theme=theme, key=key)))

# THEME 1 — toolchain
n('gccmanual','Using the GNU Compiler Collection (GCC) — incl. Optimize Options chapter and -fstack-usage','GNU Project / FSF','living','official-doc','trunk','toolchain;optimization;memory-management','verified','Observed GCC 17.0.0 pre-release (2026); cite manual for exact flag behavior','gcc.gnu.org/onlinedocs/gcc','KEY')
n('clangdocs',"Clang Compiler User's Manual / Cross-compilation / Command Line Reference",'The LLVM Project','living','official-doc','trunk','toolchain','verified','Observed 23.0.0git','clang.llvm.org','KEY')
n('picolibc','Picolibc documentation','K. Packard / picolibc project','2023','official-doc','c-leaf','toolchain','verified','(c)2018-2023; Newlib+AVR-Libc blend; merged to GCC 16 codebase per Phoronix 2026-01-05','github.com/picolibc/picolibc','KEY')
n('abiaa','ARM Application Binary Interface (ABI-AA) suite','Arm Ltd','living','official-doc','trunk','toolchain;binary-linker','verified','Umbrella: AAPCS32/64, AAELF, CPPABI32, RTABI32, EHABI32, C Library ABI, semihosting; CC BY-SA 4.0','github.com/ARM-software/abi-aa','KEY')
n('barrmassa','Programming Embedded Systems: With C and GNU Development Tools, 2nd ed.','M. Barr & A. Massa','2007','book','trunk','toolchain','verified','Shared node (emb-arch)','OReilly, ISBN 978-0-596-00983-0','KEY')
n('simmonds','Mastering Embedded Linux Programming, 3rd ed.','C. Simmonds','2021','book','trunk','toolchain','verified','Linux-focused; toolchain mechanics transfer; shared node','Packt')
n('samekcourse','Modern Embedded Systems Programming video course','M. Samek (Quantum Leaps)','living','course','trunk','toolchain','verified','Startup code, vector tables, C-vs-C++ polymorphism at machine level; spans trunk + cpp-leaf; shared node','state-machine.com','KEY')
n('crosstoolng','crosstool-NG documentation','crosstool-ng project','living','official-doc','trunk','toolchain','verified','','crosstool-ng.github.io')
# THEME 2 — optimization
n('thinlto','ThinLTO documentation','Clang/LLVM Project','living','official-doc','trunk','optimization','verified','-flto=thin; cache; gold/lld/ld64 integration','clang.llvm.org/docs/ThinLTO.html','KEY')
n('thinltoblog','ThinLTO: Scalable and Incremental LTO (blog + LLVM Dev Meeting 2016 talk)','T. Johnson, M. Amini & D. Li','2016','report','trunk','optimization','verified','2016-06-20','blog.llvm.org','KEY')
n('csmith','Finding and Understanding Bugs in C Compilers (Csmith)','X. Yang, Y. Chen, E. Eide & J. Regehr','2011','paper','trunk','optimization','verified','325+ bugs reported; every compiler crashed and miscompiled','PLDI 2011 pp.283-294, DOI 10.1145/1993498.1993532','KEY')
n('godbolt','Compiler Explorer + What Has My Compiler Done for Me Lately? (CppCon 2017)','M. Godbolt','2017','course','trunk','optimization','verified','Codegen-inspection methodology; shared node (emb-cpp)','godbolt.org','KEY')
# THEME 3 — debugging
n('gdbmanual','Debugging with GDB, Tenth Edition','Free Software Foundation','living','official-doc','trunk','debugging','verified','Observed GDB v18.0.50 (2026); remote serial protocol, gdbserver','sourceware.org/gdb','KEY')
n('openocd',"OpenOCD User's Guide",'Open On-Chip Debugger project','living','official-doc','trunk','debugging','verified','Observed 0.12.0+dev (2026); JTAG/SWD, flash, GDB server','openocd.org','KEY')
n('hardfaultblog','How to debug a HardFault on an ARM Cortex-M MCU','C. Coleman','living','guide','trunk','debugging','verified','Memfault Interrupt blog','interrupt.memfault.com','KEY')
n('binutilsblog','GNU Binutils: the ELF Swiss Army Knife','Memfault Interrupt blog','living','guide','trunk','debugging','verified','objcopy/objdump/readelf/nm/size on firmware','interrupt.memfault.com')
n('semihosting','Semihosting for AArch32 and AArch64','Arm Ltd (ABI-AA)','2020','official-doc','c-leaf','debugging','verified','Version 2019Q4, dated 2020-01-30','github.com/ARM-software/abi-aa')
# THEME 4 — binary / linker
n('ld','The GNU Linker (ld)','S. Chamberlain et al., GNU Project/FSF','living','official-doc','trunk','binary-linker','verified','Observed Binutils 2.37-2.46; SECTIONS/MEMORY/KEEP, VMA/LMA, --gc-sections','sourceware.org/binutils/docs/ld','KEY')
n('lld','LLD — The LLVM Linker','LLVM Project','living','official-doc','trunk','binary-linker','verified','Observed 23.0.0git; GNU-compatible','lld.llvm.org')
n('itaniumabi','Itanium C++ ABI','Itanium C++ ABI group','living','official-doc','cpp-leaf','binary-linker','verified','Vtables, mangling, __cxa_* runtime, guard variables, RTTI; used by GCC & Clang','itanium-cxx-abi.github.io','ABSOLUTELY KEY')
n('aapcs','Procedure Call Standard for the Arm Architecture (AAPCS)','Arm Ltd (ABI-AA)','2020','official-doc','trunk','binary-linker','verified','aapcs32 2020Q2; aapcs64','github.com/ARM-software/abi-aa','KEY')
n('ehabi32','Exception Handling ABI for the Arm Architecture (EHABI32)','Arm Ltd (ABI-AA)','2018','official-doc','cpp-leaf','binary-linker','verified','2018Q4; table-based unwinding, Itanium-model based','github.com/ARM-software/abi-aa','KEY')
n('elfspec','Tool Interface Standard (TIS) ELF Specification, Version 1.2 (+ System V gABI)','TIS Committee','1995','official-doc','trunk','binary-linker','verified','May 1995; gABI live URL not directly fetched','refspecs.linuxfoundation.org/elf/elf.pdf','KEY')
n('dwarf5','DWARF Debugging Information Format, Version 5','DWARF Committee','2017','official-doc','trunk','binary-linker','verified','Feb 2017; v6 working draft (2023) in progress','dwarfstd.org')
n('levine','Linkers and Loaders','J.R. Levine','1999','book','trunk','binary-linker','verified','Hosted-oriented; mechanics transfer to embedded','Morgan Kaufmann, ISBN 978-1-55860-496-4','KEY')
n('stevanovic','Advanced C and C++ Compiling','M. Stevanovic','2014','book','trunk','binary-linker','verified','','Apress, ISBN 978-1-4302-6667-9','KEY')
n('lippman','Inside the C++ Object Model','S.B. Lippman','1996','book','cpp-leaf','binary-linker','verified','Vtables, object layout, ctor/virtual implementation','Addison-Wesley, ISBN 978-0-201-83454-3','KEY')
n('kormanyos','Real-Time C++, 4th ed.','C.M. Kormanyos','2021','book','cpp-leaf','binary-linker','verified','Startup, memory, optimization with GCC; shared node (emb-cpp)','Springer, ISBN 978-3-662-62995-6','KEY')
n('zerotomain','From Zero to main() series','F. Baldassari et al.','2019','guide','trunk','binary-linker','verified','Verified posts 2019: Bare metal C; Linker scripts; Bootloader; Newlib; Bare metal Rust','interrupt.memfault.com','VERY KEY')
n('taylorlinkers','Linkers (20-part series)','I.L. Taylor','2007','guide','trunk','binary-linker','verified','airs.com/blog archives 38-57; TLS, LTO, COMDAT, C++ templates, gold','airs.com/blog','ABSOLUTELY KEY')
n('maskray','All about... linker series (TLS, GOT, PLT, COMMON symbols)','F. Song (MaskRay)','2022','guide','trunk','binary-linker','verified','Verified posts 2021-02-14 to 2022-02-06','maskray.me','KEY')
# THEME 5 — memory management
n('dlmalloc','A Memory Allocator (dlmalloc essay)','D. Lea','2000','guide','trunk','memory-management','verified','Orig. 1987; boundary tags, binning','gee.cs.oswego.edu/dl/html/malloc.html','KEY')
n('tlsf','TLSF: a New Dynamic Memory Allocator for Real-Time Systems','M. Masmano, I. Ripoll, A. Crespo & J. Real','2004','paper','trunk','memory-management','verified','Theta(1) alloc/dealloc','ECRTS 2004 pp.79-88, DOI 10.1109/ECRTS.2004.35','KEY')
n('freertosheap','FreeRTOS memory management (heap_1 ... heap_5)','FreeRTOS project / Amazon','living','official-doc','trunk','memory-management','verified','','freertos.org')
n('bloaty','Bloaty McBloatface','J. Haberman / Google','living','guide','trunk','memory-management','verified','ELF/DWARF size profiler; shared node (emb-cpp)','github.com/google/bloaty','KEY')
n('puncover','puncover','H. Behrens','living','other','trunk','memory-management','verified','Per-function code/stack/static footprint','github.com/HBehrens/puncover')
n('llvmeh','Exception Handling in LLVM','The LLVM Project','living','official-doc','cpp-leaf','debugging','verified','Itanium EH model, landingpad, personality, LSDA','llvm.org/docs/ExceptionHandling.html','KEY')
# Unverified / to confirm
def U(id,t,a,y,typ,tier,theme,note='',ident=''):
    n(id,t,a,y,typ,tier,theme,'unverified',note,ident)
U('eafparm','Embedded Artistry posts (Demystifying ARM Floating Point Compiler Options; libmemory docs)','Embedded Artistry','UNRESOLVED','blog','trunk','toolchain','Series/author verified; exact titles not','embeddedartistry.com')
U('an4989','AN4989 STM32 microcontroller debug toolbox','STMicroelectronics','UNRESOLVED','report','trunk','debugging','App-note number/title not individually confirmed')
U('segger','SEGGER J-Link User Guide (UM08001), SystemView (UM08027), RTT documentation','SEGGER','UNRESOLVED','official-doc','trunk','debugging','Document numbers unconfirmed')
U('maskraygc','MaskRay posts on linker garbage collection and COMDAT/section groups','F. Song (MaskRay)','UNRESOLVED','blog','trunk','binary-linker','Series verified; these titles not')
U('memfaultsize','Code Size Optimization: GCC Flags','Memfault Interrupt blog','UNRESOLVED','blog','trunk','optimization','Exact title unconfirmed')
U('bootlin','Bootlin Embedded Linux system development training slides','Bootlin','living','course','trunk','toolchain','Also an emb-arch lead — merged')
U('probetools','probe-rs documentation; pyOCD docs; Black Magic Probe docs','probe-rs; pyOCD; 1BitSquared','living','official-doc','trunk','debugging','Grouped lead as listed by the report')
U('zephyrlinker','Zephyr docs on linker scripts / code relocation','Zephyr Project','living','official-doc','trunk','binary-linker','Specific pages unconfirmed')
U('gnuinternals','GNU (GCC) Internals manual','GNU Project','living','official-doc','trunk','toolchain','High-confidence, not fetched')
U('lldbdocs','LLDB documentation (remote debugging)','LLVM Project','living','official-doc','trunk','debugging','High-confidence, not fetched')
U('newlib','newlib / newlib-nano documentation','newlib project','living','official-doc','c-leaf','toolchain','High-confidence, not fetched')
U('cmake','CMake cmake-toolchains(7) cross-compile toolchain files','Kitware','living','tooling-doc','trunk','toolchain','Also an emb-cpp lead — merged')
U('dreppermem','What Every Programmer Should Know About Memory','U. Drepper','2007','report','trunk','memory-management','Strongly believed extant, not fetched')
U('wilsonsurvey','Dynamic Storage Allocation: A Survey and Critical Review','P. Wilson, M. Johnstone, M. Neely & D. Boles','1995','paper','trunk','memory-management','IWMM 1995; referenced by dlmalloc/TLSF, not directly fetched')
U('csapp',"Computer Systems: A Programmer's Perspective, 3rd ed. (linking chapter)",'R. Bryant & D. O\'Hallaron','2016','book','trunk','binary-linker','Not fetched this pass','Pearson')
# drepperlibs lead merged into emb-c verified node — see build.py.
