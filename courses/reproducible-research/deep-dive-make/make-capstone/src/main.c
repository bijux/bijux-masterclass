#include <stdio.h>
#include "util.h"
#include "sub.h"

int main(void) {
    printf("%d\n", util_add(2, 3) * sub_mult(2, 5)); /* 5 * 10 = 50 */
    return 0;
}
