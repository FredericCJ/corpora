/* config/rt_prelude_poison.h — the RT-plane poison prelude (audio-rt-ground)
 * ===========================================================================
 * WHAT. The compile-time leg of the RT guard: makes a direct call to any
 * banned operation family a COMPILE ERROR inside an RT-core translation
 * unit. Rule table: reference/rt_plane_rules_manifest.md section R2; guard
 * machinery: section R4. Reasoning root: booklet section 15.2 ("the poison
 * headers"), operationalizing booklet invariant 1.
 *
 * HOW IT IS APPLIED (by the build system, not politeness — booklet 15.2).
 * RT-core TU class ONLY (TU classes: reference/toolchain_build_manifest.md
 * section B1). The toolchain file forces it in front of every RT-core TU:
 *
 *     clang -std=c17 ... -include config/rt_prelude_poison.h core/<tu>.c
 *
 * [MEASURED 2026-08-12, clang 22.1.8 CLANG64: -include prepends this file
 * and the poison fires as documented below.]
 * - RT-ADAPTER TUs (device-loop code that must see OS headers: ALSA,
 *   mmdeviceapi.h) do NOT get this prelude — an OS header included after it
 *   could trip poison on unrelated declarations. They are covered by the
 *   --wrap interposition net + review (R4) and the include audit (G3).
 * - Control-plane TUs never see this file.
 * - Ship builds KEEP this prelude (it costs nothing); it is the --wrap net
 *   that is compiled out [booklet 15.2].
 *
 * THE ORDERING RULE (the one way to misuse this file).
 * #pragma GCC poison rejects EVERY occurrence of an identifier AFTER the
 * pragma — including declarations inside system headers. So every system
 * header an RT-core TU is allowed to use is pre-included in the BLESSED
 * BLOCK below, before the poison block; the TU's own #include of the same
 * header is then a guard no-op. Poison identifiers, not headers — the
 * pragma takes identifier tokens only.
 * [MEASURED 2026-08-12, clang 22.1.8: poison-then-#include <stdlib.h> fails
 * at stdlib.h:457 "void *__cdecl malloc(size_t)" with "attempt to use a
 * poisoned identifier"; include-then-poison compiles clean; a later USE of
 * a poisoned identifier fails at the use site with the same diagnostic.]
 * Consequence, by design: a NON-blessed header that mentions a poisoned
 * identifier — declaration, #define, or #undef — detonates at ITS OWN line:
 * the poison block doubles as a header firewall for RT-core TUs.
 * [MEASURED 2026-08-12: #include <stdio.h> after this prelude fails at
 * stdio.h:14 "#undef snprintf" on CLANG64.] Adding a header to the blessed
 * block is a reviewed change (cards/review-code.md). One documented leak in
 * the firewall [MEASURED 2026-08-12]: on x86-64, immintrin.h transitively
 * pre-includes <stdlib.h> (mm_malloc.h), so a later #include <stdlib.h> is
 * a guard no-op instead of an error — the USE ban still holds (malloc use
 * errors at the use site) and is the load-bearing mechanism for the
 * allocation family.
 *
 * WHAT POISON CANNOT CATCH (why the runtime net exists — R4).
 * Calls reached through function pointers or precompiled third-party code;
 * and expansions of macros DEFINED BEFORE the poison that merely contain a
 * poisoned identifier [ESTABLISHED: GCC cpp manual, "Pragmas" — pre-poison
 * macro expansions are exempt]. The --wrap interposition net catches those
 * at run time; the two overlap by design [booklet 15.2].
 *
 * DELIBERATELY NOT POISONED (the allowlist — R2 notes):
 * - memcpy/memmove/memset/memcmp: bounded, stateless, no locks — the blessed
 *   bulk-move primitives of the RT plane.
 * - math.h: allowed on the RT plane, but determinism-relevant (golden-
 *   mastered) paths call the vendored kernels instead — see
 *   reference/dsp_kernel_patterns_manifest.md section K6.
 * - alloca / VLAs: banned (R2) but not poisonable — alloca is a macro over
 *   __builtin_alloca on both legs [MEASURED 2026-08-12: clang64 malloc.h
 *   line 238]. Routed compiler-catchable instead: -Werror=vla -Werror=alloca
 *   in the RT-core flag row (toolchain_build_manifest section B2/B3)
 *   [MEASURED 2026-08-12: both diagnostics fire on clang 22.1.8].
 * - OS blocking calls not listed below (select/poll/epoll_wait, ReadFile,
 *   socket calls): unreachable from RT-core TUs anyway — core is OS-free
 *   (booklet invariant 8) and the include + symbol audits (G3) enforce that;
 *   poisoning common words like `select` would collide with legitimate
 *   local identifiers.
 */
#ifndef AUDIO_RT_PRELUDE_POISON_H
#define AUDIO_RT_PRELUDE_POISON_H

#ifdef __cplusplus
#error "rt_prelude_poison.h guards C17 RT-core TUs; C++ (exceptions/unwind, R2) has no place on the RT plane"
#endif

/* ---- BLESSED BLOCK -------------------------------------------------------
 * The complete system-header surface of an RT-core TU. stdlib.h, stdio.h,
 * locale.h, threads.h, setjmp.h, signal.h, time.h are deliberately absent.
 * Extend only by review (R2/R4; cards/review-code.md). */
#include <assert.h>     /* dev-build checks; expansion uses internal symbols,
                           not the poisoned `abort` token */
#include <float.h>
#include <limits.h>
#include <math.h>       /* allowlist note above; K6 owns determinism rule */
#include <stdalign.h>
#include <stdatomic.h>  /* R6 blessed ordering idioms */
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>     /* memcpy/memset allowlist; strtok still poisoned */
#if defined(__x86_64__) || defined(_M_X64)
#include <immintrin.h>  /* SIMD kernels (K5) + FTZ/DAZ thread init (R5);
                           NOTE: transitively includes stdlib.h — see the
                           firewall-leak note in the header comment */
#endif

/* Marker: lets diagnostics and audits assert the prelude is in force. */
#define AUDIO_RT_POISONED 1

/* ---- POISON BLOCK --------------------------------------------------------
 * One pragma group per banned family; each cites its row in
 * reference/rt_plane_rules_manifest.md section R2. #pragma GCC poison works
 * on clang [MEASURED 2026-08-12, clang 22.1.8 CLANG64]. */

/* R2 "allocation" — allocator locks + syscalls; RT memory is pre-claimed
 * and resident (invariant 3). Use: arenas/pools/scratch, memory M2-M4. */
#pragma GCC poison malloc calloc realloc free aligned_alloc
#pragma GCC poison strdup strndup _strdup posix_memalign _aligned_malloc _aligned_free

/* R2 "file/console IO" — syscall-backed, buffered, lock-taking. Use: flight
 * ring events (observability O2/O3), drained off-plane. */
#pragma GCC poison fopen freopen fclose fread fwrite fseek ftell rewind
#pragma GCC poison fflush setvbuf setbuf remove rename tmpfile tmpnam
#pragma GCC poison puts fputs fputc putc putchar fgets fgetc getc getchar ungetc gets perror

/* R2 "formatting (printf family, locale)" — unbounded cost, locale locks,
 * allocation. Use: event id + raw values into the ring; render off-plane
 * (O2, error_tracing E6). */
#pragma GCC poison printf fprintf sprintf snprintf vprintf vfprintf vsprintf vsnprintf
#pragma GCC poison scanf fscanf sscanf vscanf vfscanf vsscanf
#pragma GCC poison setlocale localeconv

/* R2 "string/stdio lazy init + hidden static state" — first call allocates
 * or races shared state. Use: caller-owned state; seeded PRNG struct passed
 * explicitly (dsp K3/K7 dither). */
#pragma GCC poison strtok strerror rand srand getenv

/* R2 "process exit" (extension row) — rips the process out from under the
 * device; the safe state is fade-to-silence (invariant 7). Use: error
 * dispositions E2; shutdown protocol concurrency C9. */
#pragma GCC poison exit _Exit quick_exit abort atexit at_quick_exit raise

/* R2 "locks/waits" + "sleep/yield" — a lock's worst case is unbounded here
 * (booklet 6.2); a yield is a scheduler donation with no contract (booklet
 * 6.7). Use: wait-free channels (concurrency C1-C6), eventcount pool (C7).
 * ISO C11 threads.h spellings. threads.h is ABSENT on CLANG64 [MEASURED
 * 2026-08-12: fatal error, file not found]; on the Linux leg (glibc) it
 * exists, is not blessed, and its inclusion detonates on these tokens: */
#pragma GCC poison mtx_init mtx_lock mtx_timedlock mtx_trylock mtx_unlock mtx_destroy
#pragma GCC poison cnd_init cnd_wait cnd_timedwait cnd_signal cnd_broadcast cnd_destroy
#pragma GCC poison thrd_create thrd_join thrd_detach thrd_sleep thrd_yield thrd_exit
#pragma GCC poison call_once tss_create tss_set
/* POSIX/NT spellings (belt-and-suspenders under invariant 8's OS-free core;
 * distinctive names only — no collision risk with local identifiers): */
#pragma GCC poison pthread_mutex_lock pthread_mutex_timedlock pthread_cond_wait pthread_cond_timedwait pthread_join
#pragma GCC poison sem_wait sem_timedwait nanosleep usleep sched_yield
#pragma GCC poison Sleep SleepEx SwitchToThread WaitForSingleObject WaitForMultipleObjects WaitOnAddress

/* R2 "dlopen/LoadLibrary" — loader lock + file IO + relocation. Use: bind
 * everything at the composition root; dispatch binds once (invariant 12). */
#pragma GCC poison dlopen dlsym dlclose
#pragma GCC poison LoadLibraryA LoadLibraryW LoadLibraryExA LoadLibraryExW GetProcAddress FreeLibrary

/* R2 "C++ exceptions/unwind" — C-side spellings of non-local control flow;
 * breaks every boundedness argument (R3). Use: result codes (error_tracing
 * E4). The C++ vector is closed by the #error above + symbol audit (G3). */
#pragma GCC poison setjmp longjmp siglongjmp

/* R2 "blocking syscalls" — shell-outs; never legitimate on any plane of a
 * shipped build. */
#pragma GCC poison system popen pclose

#endif /* AUDIO_RT_PRELUDE_POISON_H */
