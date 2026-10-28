
#ifndef FRAMEVAULT_H
#define FRAMEVAULT_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define FV_OK 0
#define FV_INVALID_ARGUMENT 1
#define FV_INVALID_ARCHIVE 2
#define FV_CALLBACK_STOPPED 3
#define FV_PANIC_CONTAINED 4

typedef struct FvSession FvSession;

typedef struct FvReport {
    uint32_t entry_count;
    uint64_t total_payload_bytes;
    size_t error_offset;
} FvReport;

typedef struct FvEntryView {
    uint8_t kind;
    const uint8_t *name_pointer;
    size_t name_length;
    const uint8_t *payload_pointer;
    size_t payload_length;
} FvEntryView;

typedef int32_t (*FvEntryCallback)(void *context, const FvEntryView *entry);

/* Returned pointer is process-lifetime, read-only, and NUL-terminated. */
const char *framevault_version(void);

/* report must be writable and must not overlap bytes[0..length). A NULL byte
 * pointer is accepted only when length is zero. */
int32_t framevault_validate(const uint8_t *bytes, size_t length, FvReport *report);
/* out_session must be writable and must not overlap bytes[0..length). On
 * success, release the returned non-NULL session exactly once with
 * framevault_free. */
int32_t framevault_open(const uint8_t *bytes, size_t length, FvSession **out_session);

/* out_count must be writable, must not alias session storage, and session must
 * remain live for the complete call. */
int32_t framevault_entry_count(const FvSession *session, size_t *out_count);
/* Each entry view and its field pointers are borrowed only for the callback.
 * The callback must not retain them, unwind, or free the active session. */
int32_t framevault_for_each_entry(
    const FvSession *session,
    void *context,
    FvEntryCallback callback
);
/* NULL is a no-op. Any non-NULL session must be live, uniquely owned by the
 * caller, and passed here exactly once with no concurrent access. */
int32_t framevault_free(FvSession *session);

#ifdef __cplusplus
}
#endif

#endif
