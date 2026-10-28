#include "../include/framevault.h"

static int32_t count_entry(void *context, const FvEntryView *entry) {
    size_t *count = (size_t *)context;
    if (count == NULL || entry == NULL) {
        return 1;
    }
    *count += 1U;
    return 0;
}

int main(void) {
    FvReport report = {0U, 0U, SIZE_MAX};
    FvSession *session = NULL;
    size_t count = 0U;
    const char *version = framevault_version();

    (void)report;
    (void)session;
    (void)count;
    (void)version;
    (void)count_entry;
    return 0;
}
